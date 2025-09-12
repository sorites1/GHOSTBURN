# Weapons

There are many different weapons and types of weapons in this game, from pistols to katanas. 

## Weapon Damage

All weapons (including unarmed) follow the same formula for damage. 
### Damage Array

Damage is expressed as an array, called a \[Damage Array\], which holds three values separated by slashes. These values correspond to the damage dealt on a Fade, Success, or Cool Success, respectively. The first number is the weapon's \[Minimum Damage\]. the second is the \[Normal Damage\], and the last is the \[Maximum Damage\].

| Minimum Damage | Normal Damage  | Maximum Damage |
| -------------- | -------------- | -------------- |
| Base Value     | Base Value x 2 | Base Value x 5 |
For example, a weapon with \[Minimum Damage\] of 5 would have a \[Damage Array\] of 5/10/25.
### Unarmed Attacks

Unarmed attacks, such as punches and kicks, are based on your Strength score. For an unarmed attack, the \[Minimum Damage\] is equal to your Strength score. \[Normal Damage\] is your Strength score times two. \[Maximum Damage\] is your Strength score times five.

| Minimum Damage | Normal Damage | Maximum Damage |
| -------------- | ------------- | -------------- |
| Strength       | Strength x 2  | Strength x 5   |
For example, a character with a Strength score of 3 would have an \[Unarmed\] \[Damage Array\] of 3/6/15.

### Firing Modes

Weapons that have multiple firing modes have a damage array for each mode. For example, a light pistol only has a damage array for \[Single Shot\], but an Ak-97 has three damage arrays, one for each \[Single Shot\], \[Burst Fire\], and \[Full Auto\].

## Firearms


| Weapon                 | Type         | Optimal Range | Single Shot | Burst Fire | Full Auto |
| ---------------------- | ------------ | ------------- | ----------- | ---------- | --------- |
| Ranco Shield Plus .380 | Light Pistol | Close         | 5/10/25     | -          | -         |
| SAW Sigma .45          | Heavy Pistol | Nearby        | 8/16/40     | -          | -         |
| AK-97                  | Rifle        | Far           | 12/24/60    | 15/30/75   | 20/40/100 |
| Beretta 9mm            |              |               |             |            |           |
