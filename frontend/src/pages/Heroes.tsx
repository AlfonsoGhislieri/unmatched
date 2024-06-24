import { Filter } from 'components/Filter';
import { Outlet } from 'react-router-dom';
import { SelectGrid } from 'components/SelectGrid';
import { allHeroes } from 'assets/DBMock';
import { useState } from 'react';

const Heroes = () => {
  const [heroesList, setHeroesList] = useState(allHeroes);

  const handleFilterChange = (heroes: string[]) => {
    setHeroesList(heroes);
  };

  return (
    <div>
      <h1>Heroes Page</h1>
      <Filter onFilterChange={handleFilterChange} items={allHeroes} />
      <SelectGrid heroes={heroesList} />
      <Outlet />
    </div>
  );
};

export default Heroes;
