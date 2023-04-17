from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from App.models import CommentModel
from django.http import HttpRequest
from App.utils.errors import HttpError, HTTPStatus
from App.models import CommentModel
import uuid


# email의 해당 row값을 리턴
async def get_by_uid(uid) -> CommentModel | None:
    row = await CommentModel.objects.aget(uid=uid)
    if not row.exists():
        raise HttpError(HTTPStatus.NOT_FOUND)
    return row


async def get_by_writerId(writerId):
    rows = CommentModel.objects.filter(writerId=writerId)
    if not rows.exists():
        raise HttpError(HTTPStatus.NOT_FOUND)
    return rows


async def get_by_videoId(videoId):
    rows = CommentModel.objects.filter(videoId=videoId)
    if not rows.exists():
        raise HttpError(HTTPStatus.NOT_FOUND)
    return rows


# TODO: Deprecated
# 접근한 사람의 uid와 댓글을 쓴 사람의 uid를 비교해서
# 올바르게 접근했다면 해당 rows 를 반환
# 아니면 잘못된 접근
async def check_correct_access(req: HttpRequest):
    writerId = req.session.get("user")
    rows = await get_by_writerId(writerId)  # writerId가 쓴 모든 rows들을 추출
    if rows == False:
        return False
    writerId_values = rows.values_list("writerId", flat=True)  # writerId들만 추출
    writerId_value = writerId_values[0]  # 한가지 writerId를 추출
    if writerId == str(writerId_value):  # 쓴 사람과 접근한 사람이 같다면 rows들을 리턴
        print("두개의 아이디가 같다")
        return rows
    else:
        print("두개의 아이디가 다르다")
        return False


# TODO: Deprecated
# 댓글을 데이터베이스에 저장
async def comment_register(req: HttpRequest):
    data = JSONParser().parse(req)
    uid = uuid.uuid4()
    writerId = req.session.get("user")
    videoId = data.get("videoId")
    content = data.get("content")

    if writerId is None or videoId is None or content is None:
        return HttpResponse("Json 양식이 잘못됐습니다.")

    newCommentModel = CommentModel()
    newCommentModel.uid = uid
    newCommentModel.writerId = writerId
    newCommentModel.videoId = videoId
    newCommentModel.content = content

    newCommentModel.save()

    return HttpResponse("댓글 생성 성공", status=201)


# TODO: Deprecated
# 해당 유저가 현재 로그인이 되어있는지 확인.
def check_log_in(req: HttpRequest):
    if req.session["user"] != "":
        return True
    else:
        return False


async def delete(comment_id, user_id: str):
    comment = await CommentModel.objects.aget(uid=comment_id)
    if comment.writerId != user_id:
        raise HttpError(HTTPStatus.FORBIDDEN, "삭제할 권한이 없습니다.")
    comment.delete()


async def update(comment_id, content, uid):
    comment = await CommentModel.objects.aget(uid=comment_id)
    if comment.writerId != uid:
        raise HttpError(HTTPStatus.FORBIDDEN, "수정 권한이 없습니다.")
    comment.content = content
    comment.save()
    return comment


async def create(video_id, user_id, content: str):
    comment = CommentModel()
    comment.videoId = video_id
    comment.writerId = user_id
    comment.content = content
    comment.uid = uuid.uuid4()
    comment = await CommentModel.objects.abulk_create([comment])
    return comment[0]
