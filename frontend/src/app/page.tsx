import Link from 'next/link';

const Home = () => {
  return (
    <div>
      <Link href='/decks'>Go to Decks Page</Link>
      <br /> <br />
      <h1>Home Page</h1>
      <p>Welcome to the Home page!</p>
    </div>
  );
};

export default Home;
