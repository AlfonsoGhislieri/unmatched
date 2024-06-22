import React, { useEffect, useState } from 'react';

interface SearchFieldProps {
  placeholder?: string;
  // eslint-disable-next-line no-unused-vars
  onSearch: (query: string) => void;
}

function Search(props: SearchFieldProps) {
  const [query, setQuery] = useState('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
    event.preventDefault();
  };

  useEffect(() => {
    props.onSearch(query);
  }, [query]);

  return <input type='text' value={query} onChange={handleInputChange} placeholder={props.placeholder} />;
}

export { Search };
