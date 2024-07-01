import Link from 'next/link';

export function generateStaticParams() {
  return [{ deck: 'houdini' }, { deck: 'genie' }, { deck: 'beowulf' }];
}

export default function Deck({ params }) {
  const { deck } = params;

  return (
    <div>
      <Link href='/'>Go to Home Page</Link>
      <br />
      <Link href='/decks'>Go to Decks Page</Link>
      <br /> <br />
      <h2>Deck Details</h2>
      <p>Deck: {deck}</p>
    </div>
  );
}
