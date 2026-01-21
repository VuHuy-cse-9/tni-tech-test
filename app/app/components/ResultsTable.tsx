type ResultItem = {
  created_at: string;
  det_box_count: number;
  vis_image_path: string;
};


export default function ResultsTable({ data }: { data: ResultItem[] }) {
  return (
    <table
      border={1}
      cellPadding={8}
      style={{ borderCollapse: 'collapse', width: '100%' }}
    >
      <thead>
        <tr>
          <th>Created At</th>
          <th>Boxes Count</th>
          <th>Image Path</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, idx) => (
          <tr key={idx}>
            <td>{new Date(row.created_at).toLocaleString()}</td>
            <td style={{ textAlign: 'center' }}>{row.det_box_count}</td>
            <td>
                {row.vis_image_path.split('/').slice(-1)[0]}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}