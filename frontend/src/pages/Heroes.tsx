import { SelectGrid, allHeroes } from 'components/SelectGrid';

import { Outlet } from 'react-router-dom';
import { SelectGridFilter } from 'components/SelectGridFilter';
import { useState } from 'react';

const Heroes = () => {
  const [heroesList, setHeroesList] = useState(allHeroes);

  const handleFilterChange = (query: string) => {
    setHeroesList(allHeroes.filter((hero) => hero.toLowerCase().includes(query.toLowerCase())));
  };

  return (
    <div>
      <h1>Heroes Page</h1>
      <SelectGridFilter onFilterChange={handleFilterChange} />
      <SelectGrid heroes={heroesList} />
      <Outlet />
    </div>
  );
};

export default Heroes;
