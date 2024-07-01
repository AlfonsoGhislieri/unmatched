import Link from 'next/link';

const Decks = () => {
  const deckList = ['houdini', 'genie', 'beowulf'];
  return (
    <div>
      <Link href='/'>Go to Home Page</Link>
      <br /> <br />
      <h1>Decks Page</h1>
      <ul>
        {deckList.map((deck) => (
          <li key={deck}>
            <Link href={`/decks/${deck}`}>{deck}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Decks;
