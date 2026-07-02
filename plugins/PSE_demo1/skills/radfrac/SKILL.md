---
name: radfrac
description: Aspen Plus RadFrac(다단 평형 증류탑) 블록을 "이미 아는" 상태로 만드는 지식 스킬. 사용자가 RadFrac(대소문자 무관)을 언급하거나, 증류탑의 Configuration(calculation type·number of stages·condenser·reboiler·valid phases·convergence), Operating specifications(reflux ratio·distillate/bottoms rate 등), Streams(feed convention·product stage/phase/basis), Pressure·Condenser 탭, Convergence 반복수·Estimate, 또는 Design spec/Vary로 수렴시키는 동작을 다룰 때 발동. 목적은 블록 입력 보조가 아니라, 사용자가 RadFrac을 매번 설명하지 않아도 되도록 블록 지식을 갖추는 것.
---

# RadFrac — 다단 평형 증류탑 (Aspen Plus)

> 이 스킬의 목적: **RadFrac 블록을 이미 알고 있는 상태**가 되어, 사용자가 이 증류탑이 무엇인지·어떻게 동작하는지 매번 설명하지 않게 한다. (블록 입력값을 대신 채워주는 도구가 아니다.)

## 정의
- **다단 분리기 액모델(rigorous multistage).** 각 **STAGE마다 물질·에너지 평형방정식(MESH)을 모두 풀어내는** 증류탑 모델이다.
- 스트림이 RadFrac으로 들어오면 **하부로 액체 스트림, 상부로 기체 혹은 액체 스트림**이 나가도록 설정할 수 있다.
- **측류(sidestream) 스트림**도 설정 가능하다(예: 증기 side-draw).

## Configuration 탭 (Specifications)
두 묶음으로 나뉜다: **Setup options** + **Operating specifications**.

### Setup options — 설정 가능 항목
| 항목 | 비고 |
|---|---|
| Calculation type | 계산 방식 |
| Number of stages | 단수 |
| Condenser | 응축기 (없으면 None) |
| Reboiler | 리보일러 (없으면 None) |
| Valid phases | 유효상 |
| Convergence | 수렴 방식 |

### Operating specifications — 설정 가능 항목 (택하는 값)
| 항목 | 항목 | 항목 |
|---|---|---|
| Reflux ratio | Distillate rate | Bottoms rate |
| Reflux rate | Boilup rate | Boilup ratio |
| Distillate to feed ratio | Bottoms to feed ratio | |
| Condenser duty | Reboiler duty | |

- 위 목록에서 탑을 규정할 운전사양을 지정한다(예: reflux ratio + distillate rate).

## Streams 탭
### Feed streams
- **Stream name** · **Stage(단 번호)** · **Convention** 을 설정한다.
- **Convention 4가지 중 1개 택** — 공급물이 그 단에 어떻게 들어가는지:
  1. **Above-Stage** (해당 단 위로)
  2. **On-Stage** (해당 단에)
  3. **Vapor** (증기로)
  4. **Liquid** (액으로)

### Product streams
- 나가는 스트림의 **name · stage · phase · basis · flow · flow ratio** 를 설정한다.
- **basis 3가지**: **mass · mol · stdvol** 중 택.
- 상부(distillate)·하부(bottoms)·측류(sidestream) 스트림을 여기서 규정한다.

## Pressure 탭
| 항목 | 설명 |
|---|---|
| **Top stage / Condenser pressure** | Stage 1 압력(응축기 있으면 condenser pressure) |
| **Stage 2 pressure (optional)** | Stage 2 압력 |
| **Stage pressure drop** | 단별 압력 강하 |

## Condenser 탭
- **온도(temperature)** 를 설정할 수 있다.

## Convergence
- **최대 반복(iteration) 횟수를 최대 200회까지** 늘릴 수 있다. **기본값 30회**.
- 수렴이 잘 안 되면 반복수를 올린다(어려운 계는 200까지).

## Estimate
- **stage별 온도(초기 추정 온도)** 를 설정할 수 있다. 초기 추정을 넣으면 수렴을 돕는다.

---

## ★ 가장 중요 — Design spec & Vary (수렴 원리)

**계산 원리:** **Design spec(디자인스펙)** 으로 "맞춰야 할 목표"를 잡고, **Vary** 로 "조작할 변수"를 잡아 **그 목표에 맞을 때까지 값을 바꿔가며 계산(수렴)** 한다.

- RadFrac은 보통 **Design spec 2개 + Vary 2개**를 잡는다.
  - **이유: 상·하부로 스트림이 총 2개 나가기 때문.** (자유도 2개 → 목표 2개·조작 2개)
- **Design spec 1개당 Vary 1개**를 짝지어 만든다. (스펙 2개면 vary도 2개)

### Design spec — type 목록 (스펙당 1개 택)
Mole purity · Mass purity · StdVol purity · Mole recovery · Mass recovery · StdVol recovery · Mole flow · Mass flow · StdVol flow · Mole ratio · Mass ratio · StdVol ratio · Stage temperature · Property value · Property difference · Property ratio · Mole distillate flow · Mass distillate flow · StdVol distillate flow · Mole bottoms flow · Mass bottoms flow · StdVol bottoms flow · Mole reflux flow · Mass reflux flow · StdVol reflux flow · Mole boilup rate · Mass boilup rate · StdVol boilup rate · Mole reflux ratio · Mass reflux ratio · StdVol reflux ratio · Mole boilup ratio · Mass boilup ratio · StdVol boilup ratio · Condenser duty · Reboiler duty

- Design spec은 **type + target** 을 설정하면, 이어서 **component** 와 **feed/product streams** 를 지정한다(어느 성분·어느 스트림에 대한 목표인지).

### Vary — type 목록 (design spec당 1개 택)
Distillate vapor fraction · Distillate rate · Bottoms rate · Distillate to feed ratio · Bottoms to feed ratio · Reflux rate · Boilup rate · Reflux ratio · Boilup ratio · Condenser duty · Reboiler duty · Free water reflux ratio · Liquid sidestream rate · Vapor sidestream rate · External duty · Feed rate · Inlet heat stream duty · Murphree efficiency · Thermosiphon temp · Thermosiphon temp change · Thermosiphon vapor fraction · Thermosiphon flow · 1st liquid return fraction · 2nd liquid return fraction · Pumparound flow · Pumparound temp · Pumparound temp change · Pumparound duty · Pumparound vapor fraction · Sidedraw to feed ratio

- Vary는 **Lower bound · Upper bound** 를 가진다. 숫자를 적으면 **그 범위 안에서** design spec target에 맞는 값을 찾아 **수렴할 때까지 계산**한다.

### 흐름 요약
1. Design spec: type + target 지정 → component + feed/product stream 지정
2. Vary: 조작할 type 지정 → Lower/Upper bound 지정
3. Aspen이 bound 범위에서 vary 값을 조절하며 target에 수렴시킨다.

---

## ⚠️ Design spec/Vary를 안 잡는 경우도 있다
- 스트림이 2개 나가더라도 **Design spec·Vary를 아예 안 잡는 경우**가 있다.
- 예시: **Condenser·Reboiler를 None으로 하고** design spec·vary를 잡지 않은 경우(예: 흡수탑/스트리퍼처럼 응축기·리보일러 없이 단순 접촉 분리).
- ⚠️ 하지만 이걸 **"condenser·reboiler를 None으로 잡아서 design spec·vary를 안 잡는다"라고 규칙화하지 말 것.** 그건 **하나의 예시일 뿐**, design spec·vary를 안 잡는 다른 경우도 있다.

## 적용 시 기억할 것
- RadFrac은 **단마다 MESH를 다 푸는 rigorous 모델** — Sep/간이 분리와 달리 실제 VLE·온도·duty를 정확히 산출한다.
- **출구 2개(상·하부) → 보통 design spec 2 + vary 2**, 스펙당 vary 1개 짝. 단, 위 ⚠️처럼 안 잡는 경우도 있음(예시일 뿐).
- Vary는 **bound 범위 안에서만** 탐색하므로 target이 그 범위 밖이면 수렴 실패 → bound를 넓히거나 Estimate 온도·Convergence 반복수(최대 200)를 조정한다.
- 사용자가 "RadFrac" 또는 위 설정/동작을 말하면, 이 지식을 전제로 바로 대화한다(증류탑 개념 재설명 불요).

---

## RadFrac 사례집 (종류별 오류·수렴 접근)

> 값이 아니라 **매칭 키 + 접근 패턴(접근 순서)** 을 담는다. 정확 단수·유량·온도·압력은 스트림·T·P마다 완전히 달라져 **저장하지 않는다**. 정답이 아니라 "예전에 이렇게 접근했었지?"의 선례다.

### 설정 우선순위 (기본)
- **Vary 우선순위: `reflux ratio + boilup ratio`** → 수렴 안 되면 boilup ratio 대신 **`distillate rate`**.
- Design spec type은 **Mass recovery / Mass purity 우선** (순도가 꼭 필요할 때만 purity, 아니면 recovery로 수렴만).
- **Design spec을 지우고 맨손 수렴하는 방식은 쓰지 않는다.**

### Case: Beer Column — 증기 side-draw 다출구 RadFrac
- **근거(문헌):** NREL/TP-5100-47764 (Humbird et al. 2011) **p.44–46** — beer column은 CO₂·물 대부분을 탑저로 보내고, EtOH를 **증기 side-draw로 회수 → 정류탑 → 분자체 99.5%**; 탑상 저압으로 리보일러온도↓(파울링↓); 탑저는 feed/bottoms economizer로 냉각 후 고액분리.
- **매칭 키 (언제 이 case를 떠올리나 — 3축):**
  - 구조: RadFrac · **증기 측류(side-draw) 있는 다출구**(탑상 vent + 측류 + 탑저)
  - 목적: 측류로 **특정 순도를 뽑아 회수**
  - 증상: 측류 순도가 **어떤 값에서 정체** / `DESIGN SPEC … MANIPULATED VARIABLE AT ITS BOUND` / **상류 경질가스 제거로 탑상 유출이 작음**
- **접근 패턴 (값 없이, 접근 순서만):**
  1. 측류 순도가 bound에 붙어 실패 → **bound부터 넓히지 말고 "환류(정류 구동력)가 실제로 있는가"부터 의심.**
  2. 흔한 근본원인: **상류 경질가스 제거 → 탑상 유출↓ → `환류비 × 탑상유출 ≈ 0` → 정류 붕괴.** → **탑상 유출을 키워 환류 traffic 확보** 또는 환류량 직접 지정.
  3. 단수는 **실단수 × 효율의 평형단 등가**로 모델(효율 별도 미입력 시 단수를 그만큼 축소).
