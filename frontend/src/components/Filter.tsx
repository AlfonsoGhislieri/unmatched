import { allIP, allSets } from 'assets/DBMock';
import { useEffect, useState } from 'react';

import { CategoryWithTagsFilter } from './CategoryWithTagsFilter';
import { Search } from './Search';

interface Props {
  items: string[];
  // eslint-disable-next-line no-unused-vars
  onFilterChange: (filteredItems: string[]) => void;
}

function Filter(props: Props) {
  const [items, setItems] = useState(props.items);

  const handleSearchChange = (query: string) => {
    setItems(props.items.filter((item) => item.toLowerCase().includes(query.toLowerCase())));
  };

  const handleSetChange = (selectedCategories: string[], visibleCategories: string[]) => {
    let visibleItems = new Array<string>();
    visibleCategories.forEach((cat) => allSets[cat].forEach((item) => visibleItems.push(item)));
    visibleItems = props.items.filter((item) => visibleItems.includes(item));

    if (selectedCategories.length == 0) setItems(visibleItems);
    else {
      let selectedItems = new Array<string>();
      selectedCategories.forEach((cat) => allSets[cat].forEach((item) => selectedItems.push(item)));
      selectedItems = props.items.filter((item) => selectedItems.includes(item));
      setItems(selectedItems);
    }
  };

  useEffect(() => {
    props.onFilterChange(items);
  }, [items]);

  return (
    <div>
      <Search onSearch={handleSearchChange} />
      <CategoryWithTagsFilter
        tagsTitle='IP'
        tags={Object.keys(allIP)}
        categoriesTitle='Sets'
        categories={Object.keys(allSets)}
        onChange={handleSetChange}
      />
    </div>
  );
}

export { Filter };
