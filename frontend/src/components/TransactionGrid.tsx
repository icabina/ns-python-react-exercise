import React, { useEffect, useState } from "react";

interface Transaction {
  id: number;
  description: string;
  amount: number;
  type: string;
  category_id: number;
  category_name: string;
  date: string;
  tags: string[];
}

const TransactionGrid: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [pageSize, setPageSize] = useState<number>(10);
  const [sortBy, setSortBy] = useState<string>("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const url = new URL(
        "http://localhost:8000/api/v1/transactions/grid-view",
      );
      url.searchParams.append("page", page.toString());
      url.searchParams.append("size", pageSize.toString());
      url.searchParams.append("sort_by", sortBy);
      url.searchParams.append("sort_order", sortOrder);

      const response = await fetch(url.toString());
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      setTransactions(data.data);
      setTotal(data.total);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [page, pageSize,sortBy, sortOrder]);

  const toggleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(column);
      setSortOrder("asc");
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  if (loading)
    return <div className="text-gray-700">Loading transactions...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg mt-8">
      <div className="px-4 py-5 sm:px-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">
          Transactions Grid
        </h3>
      </div>
      <div className="border-t border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {[
                "date",
                "type",
                "category_name",
                "description",
                "amount",
                "tags",
              ].map((col) => (
                <th
                  key={col}
                  onClick={() => toggleSort(col)}
                  className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                >
                  {col.replace("_", " ").toUpperCase()}{" "}
                  {sortBy === col ? (sortOrder === "asc" ? "▲" : "▼") : ""}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((t) => (
              <tr key={t.id}>
                <td className="px-6 py-4 text-center text-sm text-gray-500">
                  {new Date(t.date).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 text-center">
                  <span
                    className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      t.type === "credit"
                        ? "bg-green-100 text-green-800"
                        : "bg-red-100 text-red-800"
                    }`}
                  >
                    {t.type}
                  </span>
                </td>
                <td className="px-6 py-4 text-center text-sm text-gray-500">
                  {t.category_name}
                </td>
                <td className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                  {t.description}
                </td>
                <td className="px-6 py-4 text-center text-sm text-gray-900">
                  ${t.amount.toFixed(2)}
                </td>
                <td className="px-6 py-4 text-center text-sm">
                  {t.tags.map((tag) => (
                    <span
                      key={tag}
                      className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mr-1"
                    >
                      {tag}
                    </span>
                  ))}
                </td>
              </tr>
            ))}
            {transactions.length === 0 && (
              <tr>
                <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                  No transactions found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
        {/* Pagination controls */}
        <div className="px-6 py-4 flex justify-between items-center">
          <button
            onClick={() => setPage(Math.max(page - 1, 1))}
            disabled={page === 1}
            className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          >
            Previous
          </button>

          <div className="px-6 py-2 flex justify-between items-center space-x-4">
            <div>
              <label className="mr-2 text-sm font-medium">
                Records per page:
              </label>
              <select
                value={pageSize}
                onChange={(e) => setPageSize(Number(e.target.value))}
                className="border px-2 py-1 rounded"
              >
                {[5, 10, 20, 50].map((size) => (
                  <option key={size} value={size}>
                    {size}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <span>
                Page 
                    <input
                        type="number"
                        min={1}
                        max={totalPages}
                        value={page}
                        onChange={(e) => {
                        let val = Number(e.target.value);
                        if (val < 1) val = 1;
                        if (val > totalPages) val = totalPages;
                        setPage(val);
                        }}
                        className="w-16 border px-2 py-1 rounded text-center"
                    />
                 of {totalPages}
              </span>
            </div>
          </div>
          <button
            onClick={() => setPage(Math.min(page + 1, totalPages))}
            disabled={page === totalPages}
            className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default TransactionGrid;
