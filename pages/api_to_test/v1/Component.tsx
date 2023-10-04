import { useTable } from 'react-table';
import supabase from '../../../lib/supabaseClient';
import React, { useEffect, useState } from 'react'; // assuming you've set this up as per the previous answer

function SupabaseTable() {
  const [data, setData] = useState([]);
  const [formData, setFormData] = useState({
    id: null, // You might want to auto-generate this or let Supabase do it
    created_at: null,
    url: '',
    user_id: null,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Retrieve the user's ID from the current session
    const session = supabase.auth.session;
    const userId = session?.user?.id;

    if (!userId) {
      console.error("User is not authenticated");
      return;
    }

    // Incorporate the user's ID into formData before inserting
    const dataToInsert = {
      ...formData,
      user_id: userId
    };

    // Insert data into Supabase
    const { data, error } = await supabase.from('api').insert([dataToInsert]);

    if (data) {
      // Refresh your table's data after inserting
      fetchData();
    } else if (error) {
      console.error('Error inserting data:', error);
    }
  };
  useEffect(() => {
    const fetchData = async () => {
      const { data, error } = await supabase.from('api').select('*');
      if (data) setData(data);
    };

    fetchData();
  }, []);

  const columns = React.useMemo(
    () => [
      { Header: 'Column Name', accessor: 'id' },
      { Header: 'User ID', accessor: 'user_id' } // Display the user_id column in your table
    ],
    [],
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns, data });

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          name="url"
          value={formData.url}
          onChange={handleChange}
          placeholder="URL"
        />
        <button type="submit">Add Record</button>
      </form>

      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default SupabaseTable;
