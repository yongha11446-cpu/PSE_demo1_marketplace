---
name: rplug
description: Aspen Plus RPlug(플러그흐름 반응기, PFR) 블록을 "이미 아는" 상태로 만드는 지식 스킬. 사용자가 RPlug(대소문자 무관)을 언급하거나, 속도론(kinetics) 기반 반응기의 Reactor type(등온·단열·열매체 등), Configuration(Multitube·가변직경·Length/Diameter·Valid phases), Reactions(POWERLAW·LHHW의 Stoichiometry·Kinetic·kinetic factor·driving force·adsorption expression) 설정을 다룰 때 발동. 목적은 블록 입력 보조가 아니라, 사용자가 RPlug을 매번 설명하지 않아도 되도록 블록 지식을 갖추는 것.
---

# RPlug — 플러그흐름 반응기 (PFR, Aspen Plus)

> 이 스킬의 목적: **RPlug 블록을 이미 알고 있는 상태**가 되어, 사용자가 이 반응기가 무엇인지·어떻게 동작하는지 매번 설명하지 않게 한다. (블록 입력값을 대신 채워주는 도구가 아니다.)

## 정의
- **속도론(kinetics) 기반 플러그흐름 반응기(PFR).** 속도식을 이용한 **미분방정식 적분**으로 반응기 길이를 따라 조성·온도 변화를 계산한다. → 반드시 **kinetics(반응 속도식)가 필요**하다.
- 계산 원리(길이방향 적분):
  1. 반응기 **입구에서 반응물들의 농도와 온도**를 읽는다.
  2. **첫 번째 미소구간(dz)**에서 속도식으로 반응속도를 계산한다.
  3. 생성물 증가·반응물 감소로 **조성을 갱신**하고, **반응열을 반영해 온도를 갱신**한다.
  4. 갱신된 조성·온도를 **다음 구간의 입력**으로 사용한다.
  5. 이 과정을 **반응기 끝까지 반복**해 최종 출구의 **조성·온도·압력**을 예측한다.
- RStoic(전환율만)·REquil(평형만)과 달리 **속도와 반응기 크기(길이·직경·체류시간)를 실제로 모사**한다. → 크기·전환율 프로파일이 필요하면 RPlug.

## 1. Specifications 탭 — Reactor type (택1)
반응기의 열적 운전방식을 아래 7가지 중 하나로 선택:

| Reactor type | 의미 |
|---|---|
| Reactor with specified temperature | 온도 지정(등온/온도 프로파일 지정) |
| Adiabatic reactor | 단열 — 열 출입 없음, 반응열이 전부 온도변화로 |
| Reactor with constant thermal fluid temperature | 열매체 온도 일정 |
| Reactor with co-current thermal fluid | 병류(co-current) 열매체 |
| Reactor with counter-current thermal fluid | 향류(counter-current) 열매체 |
| Reactor with specified thermal fluid temperature profile | 열매체 온도 프로파일 지정 |
| Reactor with specified external heat flux profile | 외부 열유속 프로파일 지정 |

## 2. Configuration 탭
- **Multitube reactor** — *아직 비활성화.* 체크하면 **Number of tubes** 입력칸이 활성화(다관식 반응기).
- **Diameter varies along the length of the reactor** — *아직 비활성화.* 체크하면 길이방향 가변직경 입력이 활성화.
- **Reactor dimensions** — **Length**, **Diameter** 입력칸. **항상 활성화**되어 있다(필수).
- **Valid phases** — Process stream 칸에서 아래 중 하나 선택:
  1. Vapor-Only
  2. Liquid-Only
  3. Vapor-Liquid
  4. Vapor-Liquid-Liquid
  5. Liquid-FreeWater
  6. Vapor-Liquid-FreeWater
  7. Liquid-DirtyWater
  8. Vapor-Liquid-DirtyWater

## 3. Reactions 탭
- Aspen 내에 미리 설정한 **Reactions(반응 세트)** 를 이 블록에 연결한다.
- 반응 세트를 **처음 생성**할 때 아래 타입 중 하나를 선택:
  CRYSTAL, EMULSION, FERMENTATION, FREE-RAD, GENERAL, IONIC, **LHHW**, **POWERLAW**, PYROLYSIS, REAC-DIST, SEGMENT-BAS, STEP-GROWTH, USER, USERACM, ZIEGLER-NAT

### POWERLAW / LHHW 공통 입력
**① Stoichiometry (반응식마다)**
- **Reactants**: Component, Coefficient
- **Products**: Component, Coefficient
- **Reaction type**: Kinetic / Equilibrium (택1)

**② Kinetic (반응식마다 — Reaction type이 Kinetic일 때)**
- **Reacting phase**: Liquid / Liquid 1 / Liquid 2 / Vapor / Liquid & Solid (택1)
- **Rate basis**: Reac (vol) / Cat (wt) (택1)

### LHHW — kinetic expression
$$r = \frac{(\text{kinetic factor}) \times (\text{driving force expression})}{\text{adsorption expression}}$$

- **Kinetic factor** — 입력칸 k, n, E, To:
  - To 지정 시: kinetic factor = k·(T/To)ⁿ · exp[ −(E/R)·(1/T − 1/To) ]
  - To 미지정 시: kinetic factor = k·Tⁿ · exp[ −E/(R·T) ]
- **Driving force expression**:
  - **[Ci] basis** (택1): molarity, mole fraction, mass fraction, partial pressure, mass concentration, mole gamma, fugacity
  - **Enter term**: **Term1, Term2 둘 다 작성** — 각 term에 생성물·반응물의 component 및 exponent 입력, 그리고 driving force 상수 계수 **A, B, C, D** 입력.
- **Adsorption expression**: adsorption expression exponent, concentration exponents, adsorption constants 입력.

## 적용 시 기억할 것
- RPlug은 **kinetics 없이는 계산 불가** — 반드시 속도식(POWERLAW/LHHW 등)이 붙은 Reactions가 있어야 한다.
- 결과는 **길이방향 프로파일**(조성·온도)로 나온다 — 최종 출구값뿐 아니라 위치별 변화도 예측한다.
- **Length/Diameter는 필수 입력**이며, 반응기 크기가 전환율을 직접 결정한다(체류시간). Multitube·가변직경은 현재 비활성, 체크 시에만 관련 입력이 열린다.
- Reactor type 선택이 온도 프로파일을 좌우한다 — 단열이면 반응열이 전부 온도변화로, 등온이면 온도 고정.
- 사용자가 "RPlug"(대소문자 무관) 또는 위 설정/동작을 말하면, 이 지식을 전제로 바로 대화한다(PFR 개념 재설명 불요).
