/* =========================
   WAR FACTS
   war(WarID, StartYear, EndYear)
   ========================= */
war(w1, 1914, 1918).
war(w2, 1939, 1945). 

/* =========================
   BATTLE FACTS
   battle(BattleName, WarID, Year)
   ========================= */

% World War I
battle('Battle of Somme', w1, 1916).
battle('Battle of Verdun', w1, 1916).
battle('Battle of Gallipoli', w1, 1915).
battle('Battle of Jutland', w1, 1916).
battle('Battle of Cambrai', w1, 1917).
battle('Battle of Passchendaele', w1, 1917).
battle('Battle of Mons', w1, 1914).

% World War II
battle('Battle of Midway', w2, 1942).
battle('Battle of Stalingrad', w2, 1942).
battle('D-Day', w2, 1944).
battle('Battle of the Bulge', w2, 1944).
battle('Battle of El Alamein', w2, 1942).
battle('Battle of Kursk', w2, 1943).
battle('Battle of Okinawa', w2, 1945).

/* =========================
   COUNTRY FACTS
   country(CountryName, TroopsNo)
   ========================= */
country('United Kingdom', 5000000).
country('France', 4200000).
country('Germany', 8000000).
country('United States', 12000000).
country('Soviet Union', 34000000).
country('Japan', 6000000).
country('Italy', 3500000).
country('Australia', 1000000).
country('Canada', 1100000).
country('Turkey', 700000).

/* =========================
   PARTICIPATION FACTS
   participation(CountryName, Role, BattleName)
   ========================= */

% WWI examples
participation('United Kingdom', defender, 'Battle of Somme').
participation('France', defender, 'Battle of Somme').
participation('Germany', attacker, 'Battle of Somme').

participation('France', defender, 'Battle of Verdun').
participation('Germany', attacker, 'Battle of Verdun').

participation('Turkey', defender, 'Battle of Gallipoli').
participation('Australia', attacker, 'Battle of Gallipoli').
participation('United Kingdom', attacker, 'Battle of Gallipoli').\

participation('United Kingdom', defender, 'Battle of Jutland').
participation('Germany', attacker, 'Battle of Jutland').

participation('United Kingdom', attacker, 'Battle of Cambrai').
participation('Germany', defender, 'Battle of Cambrai').

participation('United Kingdom', attacker, 'Battle of Passchendaele').
participation('France', attacker, 'Battle of Passchendaele').
participation('Germany', defender, 'Battle of Passchendaele').

participation('United Kingdom', defender, 'Battle of Mons').
participation('Germany', attacker, 'Battle of Mons').

% WWII examples
participation('United States', attacker, 'Battle of Midway').
participation('Japan', defender, 'Battle of Midway').

participation('Soviet Union', defender, 'Battle of Stalingrad').
participation('Germany', attacker, 'Battle of Stalingrad').

participation('United States', attacker, 'D-Day').
participation('United Kingdom', attacker, 'D-Day').
participation('France', attacker, 'D-Day').
participation('Germany', defender, 'D-Day').

participation('Germany', attacker, 'Battle of the Bulge').
participation('United States', defender, 'Battle of the Bulge').
participation('United Kingdom', defender, 'Battle of the Bulge').

participation('United Kingdom', attacker, 'Battle of El Alamein').
participation('United States', attacker, 'Battle of El Alamein'). 
participation('Germany', defender, 'Battle of El Alamein').
participation('Italy', defender, 'Battle of El Alamein').

participation('Soviet Union', defender, 'Battle of Kursk').
participation('Germany', attacker, 'Battle of Kursk').

participation('United States', attacker, 'Battle of Okinawa').
participation('Japan', defender, 'Battle of Okinawa').



/* =========================
   ALLIANCE FACTS
   alliance(Country1, Country2, AllianceID, WarID, AllianceType)
   ========================= */

% WWI
alliance('United Kingdom', 'France', a1, w1, allies).
alliance('Germany', 'Austria-Hungary', a2, w1, central_powers).

% WWII
alliance('United States', 'United Kingdom', a3, w2, allies).
alliance('Soviet Union', 'United States', a4, w2, allies).
alliance('Germany', 'Italy', a5, w2, axis).
alliance('Germany', 'Japan', a6, w2, axis).


/* =========================
   Rules
   ========================= */
% Find all battles in a war
battles_in_war(WarID, BattleName) :-
    battle(BattleName, WarID, _).

% Find all countries in a battle
countries_in_battle(BattleName, Country) :-
    participation(Country, _, BattleName).

% Find all countries in a war
countries_in_war(WarID, Country) :-
    battle(BattleName, WarID, _),
    countries_in_battle(BattleName, Country).

% Find all wars a country has fought in
wars_of_country(Country, WarID) :-
    participation(Country, _, BattleName),
    battle(BattleName, WarID, _).

% Finding the number of Troops
total_troops(Country1, Country2, Total) :-
    country(Country1, Troops1),
    country(Country2, Troops2),
    Total is Troops1 + Troops2.
    
% War duration (inclusive)
war_duration(WarID, Years) :-
    war(WarID, Start, End),
    Years is End - Start + 1.
   
% Alliance side membership (individual countries)
side_country(WarID, Side, Country) :-
    alliance(C1, C2, _AId, WarID, Side),
    (Country = C1 ; Country = C2).