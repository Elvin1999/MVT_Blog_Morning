
from dataclasses import dataclass,field
from datetime import datetime
from typing import List,Optional

@dataclass
class Post:
    id: int
    title: str
    content: str
    author: str = "anonymous"
    created_at: datetime=field(default_factory=datetime.now)
    updated_at: Optional[datetime]=None

# in memory store
_POSTS:List[Post]=[]
_NEXT_ID:int=1

def _next_id():
    global _NEXT_ID
    nid=_NEXT_ID
    _NEXT_ID+=1
    return nid

# CRUD helpers

def all_posts()->List[Post]:
    return sorted(_POSTS,key=lambda post: post.created_at,reverse=True)

def get_post(pid:int)->Optional[Post]:
    return next((p for p in _POSTS if p.id==pid),None)

def add_post(title:str,content:str,author:str="anonymous")->Post:
    p=Post(id=_next_id(),title=title.strip(),content=content.strip(),author=author.strip() or "anonymous")
    _POSTS.append(p)
    return p

def update_post(pid:int,title:str,content:str,author:str)->Optional[Post]:
    p=get_post(pid)
    if not p:
        return None
    p.title=title.strip()
    p.content=content.strip()
    p.author=(author.strip() or "anonymous").strip()
    p.updated_at=datetime.now()
    return p

def delete_post(pid:int)->bool:
    p=get_post(pid)
    if not p:
        return False
    _POSTS.remove(p)
    return True

def seed():
    if _POSTS:
        return

    add_post('Welcome','This is simple Blog example','Elvin')
    add_post('Django MVT','Today, we are practising View Template Url','Aysel')

