# 物件導向名詞

簡介物件導向的名詞，以 TypeScript 為例。

## 種類

介紹各種你會看到的名詞。

### 類別

Class，類別，一種可以整合邏輯和狀態的單位，例如：

```typescript
// 類別名稱，貴賓狗
class Poodle {
  // 靜態公開屬性，正常的貴賓狗的腿數
  public static legs = 4;

  // 公開屬性，這個貴賓狗的腿數
  public legs: number;

  // 私有屬性，這個貴賓狗的能量
  private energy: number;

  // 建構子
  constructor(legs = Poodle.legs, energy = 10) {
    this.legs = legs;
    this.energy = energy;
  }

  // 公開函式，貴賓狗呼叫
  public shout(): string {
    this.shoutCost();
    return 'woof';
  }

  // 公開函式，這隻貴賓狗受傷了嗎
  public isInjured() {
    return Poodle.legs > this.legs;
  }

  // 公開函式，這隻貴賓狗是不是累了
  public isTired(): boolean {
    return this.energy < 5;
  }

  // 私有函式，當叫了之後會消耗的東西
  private shoutCost(): void {
    this.energy -= 3;
  }
}
```

接著你可以這樣操作：

```typescript
// 建構實例，常說 new 一個 instnace
const poodle = new Poodle(3);
// 使用公開函式
console.log(`Is injured? ${poodle.isInjured()}`);
console.log(`Shout: ${poodle.shout()}`);
console.log(`Is tired? ${poodle.isTired()}`);
console.log(`Shout: ${poodle.shout()}`);
console.log(`Is tired? ${poodle.isTired()}`);
// 使用公開屬性
console.log(`Legs should have: ${Poodle.legs}, but get ${poodle.legs}`);
// 以下操作會出錯
poodle.energy;
poodle.shoutCost();
```

有幾點名詞：

- new（construct），建構，建構出來的會稱為一個實例（instance）或物件（object）
- attribute（property），屬性，實例專屬的值
- method（function），函式，實例專屬的函式
- public，公開，外部操作實例可以用的函式，也可以在類別內部使用
- private，私有，只有類別內部可以使用

### 抽象類別

把類別抽象化，例如：

```typescript
abstract class Dog {
  public static legs = 4;

  public legs: number;

  // 注意這裡從 private 改成 protected
  protected energy: number;

  constructor(legs = Dog.legs, energy = 10) {
    this.legs = legs;
    this.energy = energy;
  }

  public shout(): string {
    this.shoutCost();
    return 'woof';
  }

  public isInjured(): boolean {
    return Dog.legs > this.legs;
  }

  // 注意這裡從 private 改成 protected
  // 除此之外，把這個函示抽象化，abstract
  protected abstract shoutCost(): void;
}

// 貴賓犬
class Poodle extends Dog {
  protected shoutCost(): void {
    this.energy -= 3;
  }
}

// 鬥牛犬
class Bulldog extends Dog {
  // 呆呆的狗種，嚎叫會消耗更多體力
  protected shoutCost(): void {
    this.energy -= 4;
  }
}
```

這裡有幾個新的名詞：

- extends（inherit），繼承，`Poodle` 或 `Bulldog` 都去繼承抽象類別 `Dog`
- protected，保護，除了類別內部使用，繼承後的類別，也可以使用這個種類的屬性或函式
- abstract，抽象，把類別、函式或屬性抽象，繼承的類別必須去**實作**（implement）他

但是抽象類別不能建構：

```typescript
// 會出錯
const dog = new Dog();
```

### 介面

除了抽象類別，你也可以用介面（interface）來把抽象程度拉高：

```typescript
interface Animal {
  legs: number;

  isInjured(): boolean;
}

// 注意這裡是用 implements 不是 extends
abstract class Dog implements Animal {}
```

- interface，介面，一種契約，會要求實作（implements）它的（抽象）類別去實作某些函式或屬性，*只需定義公開函式或屬性*

介面一樣不能建構：

```typescript
// 會出錯
const animal = new Animal();
```

這裡再強調一下**介面本身沒有實作**，介面只是告訴大家：我有這個函式，但其他人怎麼實作的我不知道。以上面的介面為例，所有 `Animal` 都可以有 `isInjured` 這個函示，並且他回傳的值必須是 `boolean`。

也因此類別必須去「實作」這個介面，以上面的抽象類別 `Dog` 為例，他就實作了這個函示：

```typescript
abstract class Dog implements Animal {
  public isInjured(): boolean {
    // 這裡的程式碼，稱為實作
    return Dog.legs > this.legs;
  }
}
```

### 比較一下

- *建構*（construct, new）和 *實作*（implements）的差別
- *私有*（private）、*保護*（protected）、*公開*（public） 的差別
- *介面*（interface） 和 *抽象類別*（abstract class） 的差別

| 種類           | 建構 | 實作 | 抽象程度 |
| -------------- | ---- | ---- | -------- |
| class          | O    | O    | 低       |
| abstract class | X    | O    | 中       |
| interface      | X    | X    | 高       |

**為什麼要拉高抽象程度？**

想像一下朋友打電話給你，問你在幹嘛，你可以有兩種選擇：

- 我在吃飯
- 我在用銀色湯匙裝著約三克、六十顆的米飯，並用右手抓著湯匙，正準備送進嘴巴並咀嚼（然後你就失去你唯一的朋友了）

從例子可以了解到，抽象的**目的是為了溝通**，當物件和物件之間溝通容易了之後，才有可能把整體的架構寫的單純簡單，例如：

```typescript
// 檢查現在的環境是不是優良的
function isGoodEnv(animals: Animal[]): boolean {
    // 找出疲倦的動物
    const tiredAnimals = animals.filter((animal) => animal.isTired());
    // 如果疲倦的動物小於總體的三成，就是好的環境
    return tiredAnimals.length / animals.length < 0.3;
}
```

除此之外，抽象之後，就可以延伸很多設計模式（Design Patterns）。

### 整合一下

雖然介面和抽象類別不能建構，但是他可以被用作型別（type）。

```typescript
// 挑逗動物，會觸法它吼叫
function influriate(animal: Animal) {
  return animal.shout();
}

const poodle = new Poodle();
console.log(influriate(poodle));
```
