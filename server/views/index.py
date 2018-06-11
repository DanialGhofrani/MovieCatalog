from flask import render_template, session
from uuid import uuid4


def indexGet():
    random_sid = uuid4()
    session['sid'] = random_sid
    return render_template(
        'index.html',
        session_id=random_sid
    )
