import * as tile from './assets/tiles';

interface CharacterTileProps {
  name: string;
}

function CharacterTile(props: CharacterTileProps) {
  const charName = props.name as keyof typeof tile;
  return <img src={tile[charName]}></img>;
}

export default CharacterTile;
