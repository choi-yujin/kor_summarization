# kor_summarization Flashback

# 개요
이화여자대학교 사이버보안 종합설계 프로젝트 진주선영 조  
23.09~24.08
인공지능을 기반으로 책 속 문장의 선호이유를 분석해주는 서비스 '플래시백'의 인공지능 모델 관련 자료를 업로드해 놓은 레포지토리입니다.

# Data
Dacon의 한국어 문서 생성 요약 경진대회의 데이터 Train Data : 34,242  Test Data : 8,501 와  
https://dacon.io/competitions/official/235673/overview/description   

AI 허브에서 제공하는 요약문 및 레포트 생성 데이터 중 문학 데이터 13200건을  
https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=582
를 학습에 사용

# Example
input: 어린왕자가 오랜 시간 동안 사랑 받은 이유는 여러 가지가 있을 수 있어요. 먼저, 이 책은 간결하면서도 깊은 의미를 담고 있어서 독자들이 공감하고 사랑하게 되었어요. 어린왕자의 이야기는 세계적인 성장과 이해의 여정을 담고 있으며, 그의 모험과 친구들을 통해 인간 본성과 인생의 의미에 대한 깊은 통찰을 전달합니다.  또한, 어린왕자의 캐릭터 자체가 매력적이고 사랑스럽기 때문에 많은 사람들이 그의 이야기에 감정적으로 연결되곤 해요. 그의 순수하고 용감한 모습, 그리고 세상에 대한 호기심과 깊은 사색은 독자들에게 용기를 주고, 소중한 가치들을 되새기게 만듭니다.  또한, 어린왕자의 이야기는 나이나 문화에 상관없이 사람들의 마음을 강하게 끌어당기는 유니버설한 메시지를 담고 있어요. 우리가 사는 세상과 인간관계, 사랑, 소외, 그리고 삶의 본질에 대한 생각을 자아내며, 독자들에게 다양한 감정과 생각을 일으키는데 이는 매우 흥미로운 요소입니다.  
output: 어린왕자의 이야기는 세계적인 성장과 이해의 여정을 담고 있으며, 그의 모험과 친구들을 통해 인간 본성과 인생의 의미에 대한 깊은 통찰을 전달한다.


# Reference
https://github.com/SKT-AI/KoBART?tab=readme-ov-file  
https://github.com/seujung/KoBART-summarization


