import 'styles/index.scss';

import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Unmatched',
  description: 'Web site created with Next.js.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en'>
      <body>
        <div id='root'>{children}</div>
      </body>
    </html>
  );
}
