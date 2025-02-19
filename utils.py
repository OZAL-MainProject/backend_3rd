import boto3
import uuid
from django.conf import settings

# 허용된 이미지 확장자
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

def is_valid_image_extension(filename):
    """파일 확장자가 허용된 이미지 형식인지 확인"""
    return filename.split(".")[-1].lower() in ALLOWED_IMAGE_EXTENSIONS

def upload_to_s3(file, folder_name):
    """S3에 이미지 업로드하는 함수 (비공개 접근)"""
    s3_client = boto3.client(
        "s3",
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    # 확장자 검증
    if not is_valid_image_extension(file.name):
        raise ValueError("허용되지 않은 파일 확장자입니다. jpg, jpeg, png만 지원됩니다.")

    file_extension = file.name.split('.')[-1].lower()
    file_name = f"{folder_name}/{uuid.uuid4()}.{file_extension}"  # 랜덤 UUID로 파일명 생성

    s3_client.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        file_name,
        ExtraArgs={"ContentType": file.content_type, "ACL": "private"}  # 비공개 설정
    )

    return file_name  # 파일명 반환 (Presigned URL이 아님)


def generate_presigned_url(s3_key, expiration=3600):
    """S3 Presigned URL 생성"""
    s3_client = boto3.client(
        "s3",
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": s3_key,
            },
            ExpiresIn=expiration,  # URL 유효시간 (기본 1시간)
        )
        return presigned_url
    except Exception as e:
        print(f"🔥 Presigned URL 생성 오류: {e}")
        return None
