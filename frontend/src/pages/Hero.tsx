import { Navigate, useParams } from 'react-router-dom';

const Hero = () => {
  const { heroId } = useParams();
  const heroList = ['houdini', 'superman', 'batman']; // Example hero names

  if (heroId && !heroList.includes(heroId)) {
    return <Navigate to='/heroes' />;
  }

  return (
    <div>
      <h2>Hero Details</h2>
      <p>Hero ID: {heroId}</p>
    </div>
  );
};

export default Hero;
