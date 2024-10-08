
<div align="center">
  <h1>GitPotato</h1>
  <img src='https://github.com/OZ-Coding-School/oz_03_main-004-FE/blob/dev/src/assets/images/jump.gif'/>
  <p>이 프로젝트는 사용자의 GitHub 및 Baekjoon 활동을 기반으로 감자 캐릭터를 성장시키는 게임형 웹 애플리케이션입니다.<br/> 사용자는 자신의 활동을 통해 감자 캐릭터를 키우고, 게임의 재미를 통해 동기 부여를 받으며 일상적인 업무와 목표를 관리할 수 있습니다.</p>
  <p><br/></p>
</div>

## 프로젝트 개요
- 프로젝트 이름: GitPotato
- 프로젝트 기간: 2024년 7월 10일~2024년 8월 4일
- 배포URL: https://www.gitpotatoes.com/
<br/>

### 팀원 구성
| **김다연**                     | **주영광**                    | **노성우**                    |
|:-------------------------------:|:-----------------------------:|:-----------------------------:|
| <img src="https://avatars.githubusercontent.com/u/164486991?v=4" width="150 radios"> | <img src="https://avatars.githubusercontent.com/u/164307740?v=4" width="150"> | <img src="https://avatars.githubusercontent.com/u/164475356?v=4" width="150"> |
| [dayeonkimm](https://github.com/dayeonkimm) | [youngkwangjoo](https://github.com/youngkwangjoo) | [NohSungwoo](https://github.com/NohSungwoo) |

<br/>

***

## 1. 기술 스택
<div>
  <img src="https://img.shields.io/badge/PYTHON-F7DF1E?style=for-the-badge&logo=PYTHON&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=Django&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/DOCKER-06B6D4?style=for-the-badge&logo=DOCKER&logoColor=blue">
</div>
<div>
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/AWS S3-569A31?style=for-the-badge">
</div>

### 협업툴
<div>
  <img src="https://img.shields.io/badge/AWS Cloudfront-5865F2?style=for-the-badge&logo=discord&logoColor=white">
  <img src="https://img.shields.io/badge/Zep-6D1ED4?style=for-the-badge">
  <img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
</div>
<br/>

## 2. 채택한 개발기술과 브랜치 전략
### 기술
- React의 컴포넌트 기반 구조와 JavaScript의 최신 기능을 활용하여 애플리케이션의 모듈화와 재사용성을 높였습니다
- Tailwind CSS의 유틸리티 클래스들을 사용하여 빠르고 일관된 스타일링을 구현했습니다
- Zustand를 활용하여 웹어플리케이션의 상태를 간단하고 직관적으로 관리했습니다, 또한 불필요한 리렌더링을 방지하고 성능을 최적화했습니다
- ESLint와 Prettier를 사용하여 코드 스타일을 자동으로 정리하고 일관성을 유지했습니다

### 브랜치 전략
- Main 프로젝트를 Fork하여 각자의 레포지토리에서 개발을 진행합니다.
- 개발을 진행할 때에는 개발 유형에 맞게 개발유형/개발구역이름 형식으로 브랜치를 생성하여 작업합니다. 예를 들어, 새로운 기능을 추가할 때는 feat/login, 버그를 수정할 때는 fix/bug123과 같은 형식을 사용합니다.
- 현재 작업하고 있는 부분의 기능 구현이 완료되면 팀원들에게 코드 리뷰를 요청합니다. Pull Request를 생성하여 코드 검토를 진행하며, 리뷰어의 피드백을 반영하여 코드를 개선합니다.
- 코드 리뷰가 완료되고 승인이 나면, Pull Request를 통해 dev 브랜치로 변경 사항을 병합합니다. 병합 후에는 dev 브랜치에서 전체적인 기능 테스트를 진행합니다. dev 브랜치의 안정성이 확보되면 main 브랜치로 병합하여 배포를 준비합니다.
- 이 전략을 통해 각 개발자는 독립적으로 작업하면서도 팀과의 협업을 원활하게 진행할 수 있습니다. 코드의 품질을 유지하고 버그를 최소화할 수 있도록 지속적으로 코드 리뷰와 테스트를 강화합니다.
<br/>

## 3. Commit Convention
| 커밋 유형    | 의미                                     | 깃모지      |
|--------------|------------------------------------------|-----------------|
| **Feat**     | 새로운 기능 추가                         |  :sparkles:   |
| **Fix**      | 버그를 고친 경우                         |  :bug:        |
| **Docs**     | 문서 수정                                |  :memo:       |
| **Refactor** | 코드 리팩토링                            |  :recycle:    |
| **Chore**    | 패키지 매니저 수정, 그 외 기타 수정      |  :package:    |
| **Design**   | CSS 등 사용자 UI 디자인 변경             |  :art:        |
| **Change**   | 파일명 변경, 파일 삭제 등 기타           |  :wrench:     |
| **Test**     | 테스트 코드, 리팩토링 테스트 코드 추가   |  :clown_face: |

<br/>

## 4. 프로젝트 구조
```
potato_project
├── app
│   ├── __init__.py
│   ├── __pycache__
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── attendances
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── baekjoons
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── common
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── management
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── commands
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       └── wait_for_db.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── githubs
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── 0003_alter_github_date.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── signals.py
│   ├── test
│   │   ├── __init__.py
│   │   └── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── potato_types
│   ├── __init__.py
│   ├── __pycache__
│   ├── actions.py
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_add_initial_data.py
│   │   ├── 0003_alter_potatotype_options.py
│   │   ├── 0003_remove_potatotype_potato_image.py
│   │   ├── 0004_merge_20240730_0318.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── potatoes
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── 0003_rename_potato_type_id_potato_potato_type.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── stacks
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0001_initial.py.save
│   │   ├── 0002_add_initial_stacks.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── views.py.save
├── todos
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── 0003_alter_todo_date.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── user_stacks
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── users
    ├── __init__.py
    ├── __pycache__
    ├── admin.py
    ├── apps.py
    │   ├── 0001_initial.py
    │   ├── 0002_alter_user_potato_level.py
    │   ├── __init__.py
    │   └── __pycache__
    ├── models.py
    ├── serializers.py
    ├── signals.py
    ├── tests.py
    ├── urls.py
    └──  views.py
```

## 5. 프로젝트
<div align="center">
  <div>
    <h3>Main Page</h3>
    <img src='https://github.com/user-attachments/assets/ea04ce83-d7eb-4a0c-89a1-03ca69ce9756'/>
  </div>
  <br/>
  <div>
    <h3>Login Page</h3>
    <img src='https://github.com/user-attachments/assets/d5477a2e-0966-4b21-867c-5731b4c005c7'/>
  </div>
    <br/>
  <div>
    <h3>Home Page</h3>
    <img src='https://github.com/user-attachments/assets/7d053635-f6be-43dd-a8f3-0f522808d7d8'/>
  </div>
  <br/>
  <div>
    <h3>Update Modal</h3>
    <img src='https://github.com/user-attachments/assets/51ff36a0-5c63-4767-9e55-058377bb77cd'/>
  </div>
  <br/>  
</div>


## 6. Architecture 및 ERD
### Architecture
![아키텍쳐](https://github.com/user-attachments/assets/57e04dea-a784-47a2-af1d-990ecc9c3ca1)


=======
# Potata Project
GitHub와 백준 활동으로 성장하는 감자 캐릭터를 키우며 생산성을 관리하는 게임형 웹 앱입니다.

## 목차
- [기능]
- [참여자]
- [라이선스]
- [연락처]

## 기능
- 사용자 감자 목록 조회, 수정, 업데이트
- 사용자 스택 조회, 수정, 업데이트
- 캘린더 조회
- Todo 조회, 추가, 수정, 삭제
- 회원가입
- 소셜 로그인, 깃허브, 백준 연동
- 로그아웃, 회원 탈퇴 (추가 예정)
- 테스트 코드 (추가 예정)
- 감자 코인 (추가 예정)
- 감자 상점 (추가 예정)
- 감자 스킨 (추가 예정)

## 참여자
- 김다연
- 노성우
- 주영광

## 라이선스
This project is licensed under the MIT License

## 연락처
- 김다연: ekdyd516@gmail.com
- 노성우: shtjddn0817@gmail.com
- 주영광: dudrknd1642@gmail.com

  ## 감자쓰 화이팅 !!!!

