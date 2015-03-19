import hashlib
import os
import json
import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from sqlalchemy.orm.exc import NoResultFound
from zope.sqlalchemy import ZopeTransactionExtension
import transaction
import pafy

from jigglypuff.celery_utils import celery
from jigglypuff.models import Song


Task_DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension())
)
engine = create_engine('sqlite:///file.db')
Task_DBSession.configure(bind=engine)


def check_song_existence(youtube_id):
    """@todo: Docstring for check_song_existence.

    :file_id: @todo
    :returns: @todo

    """
    if (youtube_id, ) in Task_DBSession.query(Song.youtube_id).all():
        return False
    else:
        return True

@celery.task
def transcode2ogg(full_file_path):
    """@todo: Docstring for transcode2ogg

    :file_id: @todo
    :returns: @todo

    """
    import os
    import subprocess

    ogg_file = full_file_path.split('.')[0] + '.ogg'
    command = 'ffmpeg -y -i ' + \
        full_file_path + \
        ' -acodec libvorbis -aq 50 ' + \
        ogg_file
    p = subprocess.Popen(command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    return ogg_file


@celery.task
def check_song_db(po):
    try:
        song = Task_DBSession.query(Song).filter_by(youtube_id=po.videoid).one()
    except NoResultFound:
        return False
    else:
        if song.status == "STARTED":
            print "Song in queue ..."
        elif song.status == "COMPLETE":
            print "Song already processed ..."
        return True


@celery.task
def start_song_db(po):
    task = Song(
        youtube_id=po.videoid,
        status='STARTED',
    )
    Task_DBSession.add(task)
    transaction.commit()


@celery.task
def complete_song_db(t):
    """@todo: Docstring for add_song_to_db.

    :arg1: @todo
    :returns: @todo

    """
    po, file_id = t
    Task_DBSession.query(Song).filter_by(youtube_id=po.videoid).update(dict(
        title=po.title,
        file_id=file_id,
        length=po.length,
        status='COMPLETE',
    ))
    transaction.commit()


@celery.task
def main_task(url, media_path, audio_format=None, Task_DBSession=Task_DBSession):
    """docstring for dl_transcode"""

    pafy_object = pafy.new(url)
    po = pafy_object
    file_id = hashlib.md5(po.videoid).hexdigest()

    # XXX no perfect locking ... atomic bomb
    if check_song_db(po):
        return 0, ''
    start_song_db(po)

    stream = po.getbestaudio()

    file_name = file_id + '.' + stream.extension
    full_file_path = os.path.join(media_path, file_name)

    r = stream.download(full_file_path)

    full_ogg_file = transcode2ogg(full_file_path)
    ogg_file = os.path.basename(full_ogg_file)
    complete_song_db.s((po, ogg_file))()

    return 0, "Song added."
