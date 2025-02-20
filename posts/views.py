import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, APIException, ValidationError
from utils import upload_to_s3
from .serializers import PostSerializer, PostDetailSerializer, PostListSerializer
from images.models import Images, PostImages
from .models import Post

# todo: trippost(detail) update, delete
# todo: modifing user pofile image post, update
# todo: modifing location get, post


class Thumbnail(APIView):
    def get(self, request):
        try:
            urls = []
            num = 0
            last_image = PostImages.objects.last()
            numbers = [ random.randint(1, last_image.id) for _ in range(100) ]
            for number in numbers:
                post = PostImages.objects.get(id=number)
                if num < 5:
                    if post.post.is_public:
                        if not post.image.url in urls:
                            urls.append(post.image.url)
                            num+=1

            return Response({'urls': urls}, status=status.HTTP_200_OK)

        except PostImages.DoesNotExist:
            return Response({'message': "url not found"}, status=status.HTTP_404_NOT_FOUND)


class TripPostView(APIView):
    """ 인증받은 유저 기준 CRUD """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        인증받은 유저가 form-data로 데이터를 보내면
        해당 내용을 MultiPartParser, FormParser를 아용하여 Parseing 하고
        upload_to_s3 함수를 이용하여 이미지 데이터만 따로 저장 및 url 확보하여
        Post 객체 생성 및 DB 저장 후 각 Image를 images table에 저장하고
        post_images table에 저장 후 HTTP_201_CREATED를 반환한다.
        """
        images = []
        response = {}

        try:
            # 본문 이미지 업로드 처리
            if "images" in request.FILES:
                post_images = request.FILES.getlist("images")  # getlist() 사용
                for image in post_images:
                    try:
                        image_url = upload_to_s3(image, "posts")
                        images.append(image_url)
                    except Exception as e:
                        raise APIException(f"Post image upload failed: {str(e)}")

            # 게시글 생성
            serializer = PostSerializer(data=request.data)
            thumbnail_url = images[0] if len(images) > 0 else None
            try:
                if serializer.is_valid():
                    post = serializer.save(user=request.user, thumbnail=thumbnail_url)
            except ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                raise APIException(f"Post creation failed: {str(e)}")

            # 이미지 정보 저장
            try:
                for image in images:
                    image_instance = Images.objects.create(url=image)
                    PostImages.objects.create(post=post, image=image_instance)
            except Exception as e:
                raise APIException(f"Post image association failed: {str(e)}")

            response["message"] = "Post created successfully"
            return Response(response, status=status.HTTP_201_CREATED)

        except NotAuthenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        except APIException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """
        인증받은 유저가 본인의 게시물을 조회하며
        만약 게시물이 없을 시 HTTP_404_NOT_FOUND를 반환한다.
        """
        try:
            posts = Post.objects.filter(user=request.user)

            if posts is None:
                return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostListSerializer(posts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            raise APIException(f"Failed to retrieve posts: {str(e)}")


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            if post.is_public == False and post.user != request.user:
                raise PermissionDenied("비공개 게시물입니다.")

            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.delete()
                return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostDetailSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Post updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            # 기본적으로 해당 user_id의 모든 Post 가져오기
            posts = Post.objects.filter(user=user_id)

            # 요청한 유저와 게시글 작성자가 다르면 공개된 게시글만 필터링
            if user_id != request.user.id:
                posts = posts.filter(is_public=True)

            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

