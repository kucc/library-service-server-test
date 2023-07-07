# library-service-server-test
KUCC Library Service Server Test Repository


models.py 파일에 아래 코드 추가
from sqlalchemy.orm import relationship

alembic 패키지 추가
alembic 초기화 작업을 위해 terminal에 다음 명령어 입력: alembic init migrations
=> migrations 폴더와 alembic.ini 파일 생성. 해당 폴더 및 파일 .gitignore에 등록 완료