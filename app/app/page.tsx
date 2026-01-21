'use client';

import { useState } from 'react';
import Navbar from './components/Navbar';

export default function Home() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;

    const formData = new FormData();
    formData.append('image', e.target.files[0]);

    setLoading(true);

    try {
      const res = await fetch('http://localhost:9988/v1/detect', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Detection failed');
      }

      // StreamingResponse → blob
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);

      setImageUrl(url);
    } catch (err) {
      console.error(err);
      alert('Upload failed: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 40 }}>

      <Navbar />

      <input type="file" accept="image/*" onChange={handleUpload} />

      {loading && <p>Processing...</p>}

      {imageUrl && (
        <img
          src={imageUrl}
          alt="Detection result"
          style={{ maxWidth: 500, marginTop: 20 }}
        />
      )}
    </main>
  );
}
