import { Link, Outlet } from 'react-router-dom';

import { CharacterGrid } from 'CharacterTile';

const Heroes = () => {
  const heroList = ['houdini', 'superman', 'batman'];
  return (
    <div>
      <h1>Heroes Page</h1>
      <ul>
        {heroList.map((hero) => (
          <li key={hero}>
            <Link to={`/heroes/${hero}`}>{hero}</Link>
          </li>
        ))}
      </ul>
      <CharacterGrid />
      <Outlet />
    </div>
  );
};

export default Heroes;
