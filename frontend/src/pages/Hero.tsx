import { CharacterTile } from 'CharacterTile';
import { useParams } from 'react-router-dom';

const Hero = () => {
  let { heroId } = useParams();

  if (!heroId) heroId = '';

  return (
    <div>
      <h2>Hero Details</h2>
      <p>Hero ID: {heroId}</p>
      <CharacterTile name={heroId} />
    </div>
  );
};

export default Hero;
