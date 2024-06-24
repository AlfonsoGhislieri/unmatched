import { useEffect, useState } from 'react';

import { CategoryFilter } from './CategoryFilter';
import { allIP } from 'assets/DBMock';

interface Props {
  tagsTitle: string;
  tags: string[];
  categoriesTitle: string;
  categories: string[];
  // eslint-disable-next-line no-unused-vars
  onChange: (selectedCategories: string[], visibleCategories: string[]) => void;
}

function CategoryWithTagsFilter(props: Props) {
  const [visibleCategories, setVisibleCategories] = useState(props.categories);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  const handleTagChange = (tags: string[]) => {
    if (tags.length == 0) setVisibleCategories(props.categories);
    else {
      const taggedCategories = new Array<string>();
      tags.forEach((tag) => allIP[tag].forEach((cat) => taggedCategories.push(cat)));
      setVisibleCategories(props.categories.filter((cat) => taggedCategories.includes(cat)));
    }
  };

  const handleCategoryChange = (selectedCategories: string[]) => {
    setSelectedCategories(selectedCategories);
  };

  useEffect(() => {
    props.onChange(
      selectedCategories.filter((cat) => visibleCategories.includes(cat)),
      visibleCategories
    );
  }, [visibleCategories, selectedCategories]);

  return (
    <div className='category-with-tags'>
      <CategoryFilter title={props.tagsTitle} categories={props.tags} onChange={handleTagChange} />
      <CategoryFilter
        title={props.categoriesTitle}
        categories={Array.from(visibleCategories)}
        onChange={handleCategoryChange}
      />
    </div>
  );
}

export { CategoryWithTagsFilter };
