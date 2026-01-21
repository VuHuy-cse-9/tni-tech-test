'use client';

import Link from 'next/link';

export default function Navbar() {
  return (
    <nav style={{ marginBottom: 20 }}>
      <Link href="/" style={{ marginRight: 20 }}>
        Upload
      </Link>
      <Link href="/results">
        Results
      </Link>
    </nav>
  );
}
