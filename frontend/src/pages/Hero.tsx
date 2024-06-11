import { useParams } from 'react-router-dom';

const Hero = () => {
  const { heroId } = useParams();

  return (
    <div>
      <h2>Hero Details</h2>
      <p>Hero ID: {heroId}</p>
    </div>
  );
};

export default Hero;
