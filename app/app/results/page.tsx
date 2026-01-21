'use client';

import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import ResultsTable from '../components/ResultsTable';

const LIMIT = 10;

export default function ResultsPage() {
  const [page, setPage] = useState(0);
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [imagePattern, setImagePattern] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);

      try {
        const params = new URLSearchParams({
          limit: LIMIT.toString(),
          offset: (page * LIMIT).toString(),
        });

        if (imagePattern.trim()) {
          params.append('image_pattern', imagePattern.trim());
        }

        const res = await fetch(
          `http://localhost:9988/results/?${params.toString()}`
        );

        if (!res.ok) throw new Error('Failed to load results');

        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error(err);
        alert('Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [page, imagePattern]);

  return (
    <main style={{ padding: 40 }}>
      <Navbar />

      <h1>Detection Results</h1>

      <input
        type="text"
        placeholder="Enter image name (e.g. 31e)"
        value={imagePattern}
        onChange={(e) => {
          setPage(0); // reset to first page when filtering
          setImagePattern(e.target.value);
        }}
        style={{
          padding: 8,
          marginBottom: 20,
          width: 300,
          display: 'block',
        }}
      />

      {loading ? (
        <p>Loading...</p>
      ) : (
        <ResultsTable data={data} />
      )}

      <div style={{ marginTop: 20 }}>
        <button
          onClick={() => setPage(p => Math.max(p - 1, 0))}
          disabled={page === 0}
        >
          Previous
        </button>

        <span style={{ margin: '0 10px' }}>
          Page {page + 1}
        </span>

        <button onClick={() => setPage(p => p + 1)}>
          Next
        </button>
      </div>
    </main>
  );
}
