import * as tile from './assets/tiles';

function CharacterGrid() {
  return (
    <div className='character-grid'>
      {heroes.map((hero) => (
        <CharacterTile name={hero} />
      ))}
      ;
    </div>
  );
}

interface CharacterTileProps {
  name: string;
}

function CharacterTile(props: CharacterTileProps) {
  const charName = props.name as keyof typeof tile;
  console.log(charName);
  if (heroes.includes(charName)) {
    return (
      <div className='character-tile'>
        <img src={tile[charName]}></img>
      </div>
    );
  } else {
    return null;
  }
}

export { CharacterTile, CharacterGrid };

const heroes = [
  'Achilles',
  'Alice',
  'Angel',
  'AnnieChristmas',
  'Beowulf',
  'Bigfoot',
  'BlackPanther',
  'BlackWidow',
  'BloodyMary',
  'BruceLee',
  'Buffy',
  'Bullseye',
  'CloakAndDagger',
  'Daredevil',
  'Deadpool',
  'Dracula',
  'DrSattler',
  'DrStrange',
  'Elektra',
  'Ghostrider',
  'GoldenBat',
  'Hamlet',
  'Houdini',
  'Ingen',
  'InvisibleMan',
  'JekyllAndHyde',
  'JillTrent',
  'KingArthur',
  'LittleRedRidingHood',
  'LukeCage',
  'Medusa',
  'MoonKnight',
  'MsMarvel',
  'NikolaTesla',
  'OdaNobunaga',
  'Raptors',
  'RobinHood',
  'Shakespeare',
  'SheHulk',
  'SherlockHolmes',
  'Sinbad',
  'Spiderman',
  'Spike',
  'SquirrelGirl',
  'SunWukong',
  'Tatiana',
  'TheGenie',
  'TomoeGozen',
  'TRex',
  'WaywardSisters',
  'Willow',
  'WinterSoldier',
  'Yennenga',
];
