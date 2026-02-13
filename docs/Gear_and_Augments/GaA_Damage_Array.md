# Damage Array

All weapons (including unarmed attacks) express damage as a \[Damage Array\].

A [[Damage Array](../Keywords/Keyword_Damage_Array.md)] holds three values separated by slashes, like this: 5/10/25. These values correspond to the damage dealt on a Fade, Success, and Cool Success, respectively. The first number is [[Minimum Damage](../Keywords/Keyword_Minimum_Damage.md)]. The second is [[Normal Damage](../Keywords/Keyword_Normal_Damage.md)], and the last is [[Maximum Damage](../Keywords/Keyword_Maximum_Damage.md)]. Refer to [Outcomes](../PtG_Outcomes.md) for more information on Fade, Success, and Cool Success.

For example, you draw your Ranco .357 Equalizer and use [Single Shot](../Skills_and_Tricks/Trick_Firearms_Core_Single_Shot.md) (a Firearms trick) to shoot at the security guard. You make a roll and score a Fade. According to the outcomes for Single Shot, a Fade deals \[Minimum Damage\]. The \[Damage Array\] for your Equalizer is 9/18/45. Since the first number in the array is 9, you deal 9 points of damage to the guard.

## Firearms Damage

Each of a weapon's firing modes has its own \[Damage Array\]. There are three firing modes and corresponding Firearms tricks: [Single Shot](../Skills_and_Tricks/Trick_Firearms_Core_Single_Shot.md), [Burst Fire](../Skills_and_Tricks/Trick_Firearms_Core_Burst_Fire.md), and [Full Auto](../Skills_and_Tricks/Trick_Firearms_Core_Full_Auto.md). Some weapons are capable of performing only in one or two of these modes; others can use all three. 

When developing new firearms for use in the game, the GM should use the formula shown in the chart below. 

| Minimum Damage | Normal Damage  | Maximum Damage |
| -------------- | -------------- | -------------- |
| Base Value     | Base Value x 2 | Base Value x 5 |

Each firing mode a weapon can use has its own Base Value. 

For example, the Graham M21-S has a Base Value of 4 for Single Shot, so its Single Shot \[Damage Array\] is 4/8/20. It has a Base Value of 9 for Burst Fire, so that \[Damage Array\] is 9/18/45. The M21-S is not capable of Full Auto, so that \[Damage Array\] is left blank.

## Brawl Damage

Damage dealt by the Brawl skill is based on your Strength score. Calculate your character's Brawl \[Damage Array\] using the formula below.

| Minimum Damage | Normal Damage | Maximum Damage |
| -------------- | ------------- | -------------- |
| Strength       | Strength x 2  | Strength x 5   |

For example, a character with a Strength score of 3 would have an [Unarmed Strike](../Skills_and_Tricks/Trick_Brawl_Core_Unarmed_Strike.md) \[Damage Array\] of 3/6/15.

## Melee Damage

Melee weapons, like knives and clubs, have their own Base Value which is added to the character's Strength score when calculating its \[Damage Array\], as shown below. 

| Minimum Damage        | Normal Damage               | Maximum Damage              |
| --------------------- | --------------------------- | --------------------------- |
| Strength + Base Value | (Strength + Base Value) x 2 | (Strength + Base Value) x 5 |

For example, a character with a Strength score of 3 is wielding a knife with a Base Value of 1. So, \[Minimum Damage\] is 4, \[Normal Damage\] is 8, and \[Maximum Damage\] is 20. The [Melee Strike](../Skills_and_Tricks/Trick_Melee_Core_Melee_Strike.md) \[Damage Array\] for this weapon when used by this character is 4/8/20.


