# PV5 GroundWatch 발표자 노트

## 1장

이 숫자 뒤에는 집으로 돌아가지 못한 한 사람이 있습니다. 우리가 찾으려는 것은 이미 생긴 구멍이 아니라, 구멍이 되기 전의 변화입니다.

[사실] 2025.3.24 18:28경 서울 강동구 명일동. 붕괴 시작 후 약 1~2분 만에 길이 22m, 폭 18m, 깊이 16m로 확대. 사망 1명, 부상 1명.
출처: 국토교통부 정책브리핑 '땅꺼짐 사고 조사결과 발표'(2025.12.3) https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996
최종보고서: https://www.molit.go.kr/USR/policyData/m_34681/dtl.jsp?id=4872

표현 원칙: 희생자 이름, 얼굴, 구조 장면은 쓰지 않습니다. 특정 기관 책임을 단정하지 않습니다. 배경은 실제 사고 사진이 아닌 개념 일러스트입니다.

## 2장

명일동 사고는 하나의 원인이 아니라 여러 조건이 겹친 결과였습니다. 직접 원인은 심층풍화대 불연속면이 만든 쐐기형 토체의 미끄러짐, 간접 원인은 터널공사로 인한 지하수위 26m 저하, 노후 하수관의 장기 누수, 강관보강 그라우팅의 지보 성능 한계입니다.

주의: 이 사고는 깊은 지질구조와 터널공사가 얽힌 사고이고, GroundWatch의 차량형 GPR은 약 2m 안팎의 얕은 공동을 주로 봅니다. 그래서 이 사고를 막을 수 있었다고 말하지 않습니다. 이 사례는 단발성 점검을 반복 관측과 변화 관리로 바꿔야 하는 이유로만 씁니다.

출처: https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996

## 3장

현재 서울시는 차량형 GPR, 수동형 GPR, 천공과 내시경을 조합해 운영합니다.
- 차량형 GPR: 서울시는 2015년 국내 처음 차량탑재형 GPR을 도입했고, 한 번 지나가며 약 3m 폭을 탐사합니다. https://news.seoul.go.kr/safe/archives/41339
- 누적 33,129km, 공동 7,760개(2014~2025.9): 경향신문 2025.10.19 https://www.khan.co.kr/article/202510191122011
- 2026년 16,423km, GPR 인력 9명→19명: 서울시 보도자료 https://www.seoul.go.kr/news/news_report.do?nttNo=454742 (언론에 나온 18,000km 계획과 차이가 있어 공식 발표 값을 씀)
- 고주파 GPR 탐지 깊이 약 2m: https://www.safetimes.co.kr/news/articleView.html?idxno=231486

## 4장

연희동 성산로 사례는 반복 관측이 왜 필요한지 보여줍니다. 서울시 설명에 따르면 이 구간은 정기점검 대상으로 2024년 5월 7일부터 16일까지 GPR 탐사차량 2대와 인력 16명을 들여 조사했지만, 당시 빈 공간이 발견되지 않았습니다. 그리고 8월 29일 함몰이 일어났습니다.
이것이 GPR 탐사의 실패라는 뜻은 아닙니다. 지하는 변하고, 한 시점의 결과는 그 시점만 말해 준다는 뜻입니다.

출처: https://www.newsis.com/view/NISX20240830_0002869815 , https://www.etoday.co.kr/news/view/2397645 , https://mediahub.seoul.go.kr/archives/2012160
[추가 확인 필요] 연희동 함몰 규모(가로, 세로, 깊이)는 공식 자료로 확인하지 못해 쓰지 않았습니다.
[가설] 아래 네 가지 공백은 현장 인터뷰로 검증합니다.

## 5장

GroundWatch는 네 단계가 반복되는 구조입니다. 새벽에 같은 경로를 순찰하고, 회차별 데이터를 위치, 깊이, 시간으로 기록해 비교하고, 전문가가 승인한 지점만 현장에서 다시 확인하고, 그 결과가 다음 순찰과 AI 개선으로 돌아갑니다.
핵심은 한 번의 탐사가 아니라 반복 관측과 변화 관리입니다.

## 6장

여기서부터는 지금 기술로 바로 꾸릴 수 있는 운영 모델 열한 가지를 순서대로 보여드립니다.

## 7장

새벽은 주차 차량과 보행자가 가장 적은 시간이라 같은 경로를 같은 조건으로 반복 주행하기 좋습니다. PV5는 전기차라 엔진 공회전 소음과 배기가스 없이 주택가를 저속으로 오래 달릴 수 있습니다.
[실증 필요] 저속 장시간 운행 시 배터리 소모와 주행거리 영향, 실제 소음 수준.
참고: https://www.kia.com/kr/vehicles/pv5-cargo/features

## 8장

PV5를 센서를 실어 나르는 차가 아니라, 탐사하고 차 안에서 분석하고 내려서 검증하는 이동형 플랫폼으로 정의합니다. 운전석의 12.9인치 PBV 전용 인포테인먼트에서 순찰 앱을 띄웁니다.
[사실] PV5 카고 롱 카고룸 2,255×1,565×1,520mm(4,420L), 적재고 419mm, 실내·실외 V2L 220V(최대 3.6kW). https://www.kia.com/kr/vehicles/pv5-cargo/specification , https://www.hyundaimotorgroup.com/ko/story/CONT0000000000178473
[설계 판단] PV5 하부는 배터리 팩이므로 GPR 안테나는 후방 오버행 하부에 다는 것을 기본안으로 하고, 배터리 케이스와 차체 금속의 간섭을 시험합니다.
[실증 필요] 적재중량, 차량총중량, 전후축 하중, 전자파 간섭, 구조변경 승인.

## 9장

4D 지하 변화지도는 도시 전체를 다 조사했다는 지도가 아닙니다. PV5가 실제로 주행하고 측정한 도로만 위치, 깊이, 시간으로 쌓습니다.
색 규칙: 회색 미조사, 초록 이전과 변화 없음, 노랑 새 이상 신호, 주황 확대 의심, 빨강 정밀 재탐사, 점선 신뢰도 낮음.
[예시] 17% 증가, 추정 깊이 0.9~1.3m, AI 신뢰도 84%는 화면 설명용 예시 값입니다.

## 10장

AI의 역할은 결론이 아니라 우선순위입니다. 수많은 GPR 데이터 가운데 이전 회차와 달라진 부분을 먼저 찾아 전문가가 볼 순서를 정합니다.
결과에는 위험등급, 변화량, 신뢰도, 위치 오차, 권장 후속조치, 전문가 승인 여부를 함께 표시하고, AI 결과와 전문가 판정을 구분합니다.
참고 연구: https://www.researchgate.net/publication/332081634
[실증 필요] 실제 탐지율, 오탐률, 미탐률은 천공 확인 결과로 측정합니다.

## 11장

AI가 찾은 후보는 바로 현장 업무가 되지 않습니다. 전문가가 원시 GPR 데이터와 함께 검토해 승인한 지점만 재확인 대기열에 들어가고, 다음 순찰 경로에 자동으로 반영됩니다.
[예시] 표의 지점 번호와 등급은 설명용입니다.

## 12장

PV5는 Android Automotive OS 기반 PBV 전용 인포테인먼트와 Pleos App Market을 지원합니다. GroundWatch Patrol은 이 환경에서 돌아가는 업무용 앱을 목표로 합니다. 완전한 독자 OS라고 표현하지 않습니다.
활용 후보 데이터: 차량 위치, 주행·주차 상태, 배터리 잔량, 충전 상태, 운행거리, 내비게이션 목적지 전달, 업무 상태.
기아와 추가 협의가 필요한 데이터: 조향각, 세부 차량 제어, ADAS 원시 데이터, 차량 카메라 원시 영상, 안전 관련 ECU 데이터.
출처: https://eu-www.kia.com/uk/pbv/solutions/software/ , https://www.kia.com/kr/pbv/solution/software ('준비 중인 솔루션' 고지), PIM 제어기 https://www.hyundaimotorgroup.com/ko/news/CONT0000000000201311 (패신저 도너모델 기준, 카고 적용은 [추가 확인 필요])

## 13장

구조는 Cloud와 PV5 Patrol 앱 사이는 보안 통신, 앱과 Edge Gateway 사이는 로컬 API, 게이트웨이와 AR 글래스 사이는 차량 내부 보안 Wi-Fi입니다.
차량 앱은 업무와 경로, 게이트웨이는 센서 데이터와 로컬 통신, AR 글래스는 현장 위치 정합과 수동 탐사 안내를 맡습니다. 이렇게 나누면 차량 API 접근이 일부 막혀도 GPR과 AR 기능 전체가 멈추지 않습니다.
[실증 필요] 앱, 게이트웨이, 글래스 사이 통신 지연과 네트워크 단절 시 오프라인 동작.

## 14장

AR 글래스는 차량이 안전하게 정차한 뒤 차 밖에서 작업자만 씁니다. 차량 안 멀미 보정은 핵심 기능에서 빼고, 글래스가 차 밖에서 독립적으로 위치를 추적합니다.
위치는 맨홀 하나로 확정하지 않고 맨홀, 차선 모서리, 경계석, RTK 좌표 중 2~3개를 결합해 보정합니다.
[실증 필요] AR 위치 정확도, 야간 기준점 인식 성능.

## 15장

작업자는 AR이 도로 위에 그린 검색 범위를 따라 양손으로 수동 GPR을 밉니다. 시작점과 종료점, 진행 방향, 반복 횟수가 보이고, 사진, 메모, 이상 위치 표시는 음성으로 처리합니다.
AR은 공동의 실제 모양을 보여주지 않습니다. 화면 아래에는 늘 '굴착 전 정밀조사와 관계기관 승인이 필요하다'는 경고를 띄웁니다.

## 16장

차량형 다채널 GPR은 넓게 선별하고, 지면 밀착형 수동 GPR은 좁은 범위를 다른 주파수와 방향으로 다시 봅니다. 수동 GPR이 늘 더 깊게 본다고 말하지 않습니다.
참고: https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/

## 17장

수동 GPR 재확인으로 공동 가능성이 높아지면 관제센터가 정밀조사를 요청하고, 도로관리기관 승인과 교통통제 뒤 천공과 내시경으로 최종 확인합니다. 결과는 복구 또는 지속 관찰로 이어지고, 다시 4D 지도에 저장돼 AI 검증 데이터가 됩니다.
승인 절차는 관할 기관 기준을 따릅니다.

## 18장

여기부터는 운영 모델이 검증된 뒤의 확장 방향입니다.

## 19장

위험도가 높은 구간일수록 순찰 주기를 짧게 잡습니다. 표의 주기는 예시이며 발주기관과 합의해 정합니다. 서울시도 명일동 사고 이후 굴착공사장 점검을 연 1회에서 월·주 단위로 강화했습니다.
출처: https://www.seoul.go.kr/news/news_report.do?nttNo=454742

## 20장

여러 대의 PV5가 권역을 나눠 운영하면 관제센터가 차량별 순찰거리, 재확인 업무, 배터리 상태를 한 화면에서 봅니다. 같은 사양의 차량이어야 권역이 달라도 데이터를 같은 기준으로 비교할 수 있습니다.
[추가 확인 필요] Pleos Fleet 또는 기관 FMS와의 연동 범위. 출처: https://www.kia.com/kr/vehicles/pv5-cargo/features

## 21장

GPR 변화 신호만으로는 원인을 알기 어렵습니다. 하수관, 굴착공사, 지하철 구조물, 지하수, 강우, 보수 이력과 겹쳐 볼 때 원인을 짐작하기 쉬워집니다. 국토부도 지하공간통합지도에 지하안전 정보를 연계하는 방향을 밝혔습니다.
지하정보는 보안 문제가 있어 팔지 않고 계약기관 대상 접근제어형 서비스로 제공합니다.
참고: https://www.ogc.org/standards/muddi/

## 22장

반복 순찰 데이터가 쌓이면 지상 지도, 지하 시설물, 공동 의심 신호, 시간에 따른 변화를 하나의 모델에서 볼 수 있습니다. 공사 전후 비교, 재난 대응, 유지관리 계획에 쓸 수 있습니다. 다만 측정한 도로에 한정하고, 측정하지 않은 구간은 비워 둡니다.

## 23장

도로가 무너진 뒤에는 누구나 구멍을 볼 수 있습니다. 우리가 찾으려는 것은 아직 보이지 않을 때 시작된 변화입니다. 한 번의 조기 발견이 한 사람의 무사 귀가가 되도록, PV5 GroundWatch를 제안합니다. 감사합니다.

## 24장

GPR의 한계를 먼저 밝힙니다.
- FHWA: 저주파는 깊고 해상도가 낮으며, 고주파는 얕고 정밀합니다. 400MHz 안테나는 최대 약 12ft. 수분과 점토가 많은 흙은 전자파를 감쇠시킵니다. 금속은 거의 모든 에너지를 반사하고 그 아래를 가립니다. https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/
- 서울시: 고주파 GPR 탐지 깊이 약 2m, 2026년부터 지하 5~40m 복합탐사를 굴착공사장 2곳에 시범 도입. https://v.daum.net/v/20251230143011653
GroundWatch는 지하철 구조 안전 검사가 아니라 역세권 도로와 공사 영향구간의 얕은 공동 감시입니다.
AI는 검토 순서를, 전문가는 판정을, 천공과 내시경은 확인을 맡습니다.

## 25장

새벽 도로에서 한 사람이 운전, 장비, 교통 확인, 수동 탐사를 모두 할 수 없습니다. 초기에는 2인 1조로 운영합니다. 주행 중 AR 사용 금지, 정차 확인 후 작업 모드, 천공과 내시경은 승인과 교통통제 뒤, 영상은 비식별화가 원칙입니다.

## 26장

1단계는 주행 거리 기반 탐사 용역, 2단계는 정기 순찰, 4D 지도, AI 변화 감지를 묶은 연간 관제 계약, 3단계는 PV5 컨버전 차량과 소프트웨어 패키지 공급입니다. 지하정보는 제3자에게 팔지 않고 계약기관이 쓰는 접근제어형 서비스로 제공합니다. 가격은 아직 정하지 않았습니다.

## 27장

출처 전체 목록(작성 기준일 2026.10.10)
1. 국토교통부 땅꺼짐 사고 조사결과 발표(2025.12.3) https://m.korea.kr/briefing/policyBriefingView.do?newsId=156732996
2. 국토교통부 명일동 사고조사 최종보고서 https://www.molit.go.kr/USR/policyData/m_34681/dtl.jsp?id=4872
3. 서울시 지반침하 예방체계 강화 https://www.seoul.go.kr/news/news_report.do?nttNo=454742
4. 서울시 연희동 사고 이후 개선안 https://mediahub.seoul.go.kr/archives/2012160
5. 서울시 차량탑재형 GPR 도입 https://news.seoul.go.kr/safe/archives/41339
6. 서울 안전누리 GPR 탐사지도 https://safecity.seoul.go.kr/distFclt/cfMapDs/cfMapDs.page?menuId=MENU_SSNS_000176
7. 뉴시스 2024.8.30 연희동 https://www.newsis.com/view/NISX20240830_0002869815
8. 경향신문 2025.10.19 서울시 GPR https://www.khan.co.kr/article/202510191122011
9. 세이프타임즈 GPR 2m https://www.safetimes.co.kr/news/articleView.html?idxno=231486
10. 서울시 복합탐사 보도 https://v.daum.net/v/20251230143011653
11. 국토부 굴착공사장 안전관리 강화방안(2025.5.27) https://www.codil.or.kr/filebank/files/202505/helpdesk/BBS_202505290920333590.pdf
12. 기아 PV5 카고 특징 https://www.kia.com/kr/vehicles/pv5-cargo/features
13. 기아 PV5 카고 제원 https://www.kia.com/kr/vehicles/pv5-cargo/specification
14. 현대차그룹 PV5의 모든 것 https://www.hyundaimotorgroup.com/ko/story/CONT0000000000178473
15. 기아 PBV 소프트웨어 https://www.kia.com/kr/pbv/solution/software
16. Kia PBV IVI와 AAOS App Market https://eu-www.kia.com/uk/pbv/solutions/software/
17. Hyundai Pleos Connect https://connected-mobility.hyundai.com/what-we-do/pleos
18. 현대차그룹 PIM 제어기 https://www.hyundaimotorgroup.com/ko/news/CONT0000000000201311
19. FHWA GPR https://infotechnology.fhwa.dot.gov/gpr-ground-penetrating-radar-utility-general/
20. OGC MUDDI https://www.ogc.org/standards/muddi/
