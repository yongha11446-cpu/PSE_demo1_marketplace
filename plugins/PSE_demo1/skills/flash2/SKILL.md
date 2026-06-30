---
name: flash2
description: Aspen Plus Flash2(2상 평형 플래시 분리기) 블록을 "이미 아는" 상태로 만드는 지식 스킬. 사용자가 Flash2(대소문자 무관)를 언급하거나, 플래시 분리기의 Specifications(Temperature·Pressure·Duty·Vapor fraction 중 2개 선택) 설정, Valid phases 설정, 또는 기상/액상 2출구 분리 동작을 다룰 때 발동. 목적은 블록 입력 보조가 아니라, 사용자가 Flash2를 매번 설명하지 않아도 되도록 블록 지식을 갖추는 것.
---

# Flash2 — 2상 평형 플래시 분리기 (Aspen Plus)

> 이 스킬의 목적: **Flash2 블록을 이미 알고 있는 상태**가 되어, 사용자가 이 분리기가 무엇인지·어떻게 동작하는지 매번 설명하지 않게 한다. (블록 입력값을 대신 채워주는 도구가 아니다.)

## 정의
- **2상 평형 플래시 분리기.** 공급물(1개 이상, 내부에서 합쳐짐)을 지정 조건에서 **상평형(VLE/VLLE)** 계산해 **기상 출구 1개 + 액상 출구 1개**로 분리한다.
- **반응 없음** — RStoic과 달리 화학반응을 풀지 않는다. 오로지 "이 조건에서 무엇이 증기로, 무엇이 액으로 갈라지는가"만 계산한다.
- 출구는 **2개**(상단=Vapor, 하단=Liquid). 고체(CISOLID substream)는 분리 없이 통과한다. (액-액 분리/물 디캔트가 필요하면 Valid phases로 제어.)

## Specifications 탭 (운전조건) — **4개 중 2개 선택**
설정할 수 있는 항목:

| 항목 | 비고 |
|---|---|
| Temperature (온도) | |
| Pressure (압력) | |
| Duty | 열부하 |
| Vapor fraction (기상분율) | |

- ⚠️ 위 4개 중 **정확히 2개를 지정**해 플래시 조건을 정의한다. 나머지 2개는 계산으로 결정된다.
- 자주 쓰는 조합:

| 조합 | 의미 |
|---|---|
| **Pressure + Temperature** | 등온 플래시 (T·P 고정, 증기량은 계산) |
| **Pressure + Vapor fraction** | 원하는 기상분율로 분리 (예: VF=0 → 이슬점 액, VF=1 → 기포점 증기) |
| **Pressure + Duty** | Duty=0이면 **단열(adiabatic) 플래시** — 감압만으로 자체 냉각 |
| **Temperature + Duty** | 온도 고정에 필요한 열부하 계산 |

- 압력을 낮추는 플래시(감압)는 **Pressure 음수 입력 = 압력강하(ΔP)**, 양수 = 절대압으로 해석(부호 규약 주의).

## Valid phases (유효상) — RStoic과 동일, 9가지 중 선택
1. Vapor-only
2. Liquid-only
3. Solid-only
4. Vapor-Liquid
5. Vapor-Liquid-Liquid
6. Liquid-free water
7. Vapor-Liquid-free water
8. Liquid-Dirty water
9. Vapor-Liquid-Dirty water

- 일반 증기-액 분리는 **Vapor-Liquid**. 물이 별도 액상으로 갈라질 가능성이 있으면 free water/Dirty water 옵션을 쓴다.

## ⚠️ 경량가스 분리 시 — Henry component 등록 (필수)
- **용존 경량가스(CO₂·O₂·N₂·H₂·CH₄·CO 등)를 액에서 기상으로 빼내는 플래시**라면, 그 가스들을 반드시 **Henry component로 등록**해야 한다.
  - 등록 위치: Properties → Components → **Henry Comps** 그룹 지정 + 용매(주로 H₂O)와의 **Henry 상수(binary)** 가 들어간 메소드 사용(NRTL-Henry·ELECNRTL 등). DB에 Henry 파라미터가 있으면 상속됨.
- **등록 안 하면 생기는 오류**: 경량가스를 일반 성분으로 보면 Aspen이 **순성분 증기압을 외삽**(CO₂는 임계점 31℃ 위라 외삽)해 VLE를 풀어 **액중 용해도를 크게 과대평가** → 빠져야 할 가스가 액에 과다 잔류한다.
- **진단법(두 가스 대조)**: 같은 플래시에서 한 가스는 잘 빠지는데(예 O₂ ~95%) 다른 가스는 안 빠지면(예 CO₂ 61%만 기상, 39% 액잔류) → **덜 빠진 가스의 Henry 미설정 의심**. 물리 검산(Henry 법칙 용해도)과 수십 배 차이면 거의 확정.
  - 실제 사례(ATJ CO₂ Flash2, 2026-06-30): CO₂ 1,372 kg/hr 중 **532 kg(39%)가 액 잔류** → 1 atm·32℃ 실제 용해도 ~18 kg의 약 29배 → Henry 미설정 원인. O₂는 94.6% 기상으로 정상.
- **점검 우선순위**: 가스 분리 Flash2가 "이상하게 많이 녹아 있으면" 운전조건(T·P)보다 **Henry component 설정부터** 확인한다.

## 적용 시 기억할 것
- Flash2는 **분리(상평형)만** — 반응·전환은 없다(필요하면 RStoic/RYield 등 반응기 블록).
- 출구가 **2개(기/액)** 라는 점이 RStoic(출구 1개)과 다르다. 증기를 따로 빼내야 할 때(예: 잠열·휘발성 억제물 제거) 적합.
- 4개 스펙 중 **2개만** 지정 — 3개 지정하면 과결정(over-specified) 오류.
- **경량가스(CO₂·O₂ 등)를 빼내는 분리면 Henry component 등록 필수** — 안 하면 용해도 과대평가로 가스가 액에 남는다(위 ⚠️ 절).
- 사용자가 "Flash2" 또는 위 설정/동작을 말하면, 이 지식을 전제로 바로 대화한다(블록 개념 재설명 불요).
