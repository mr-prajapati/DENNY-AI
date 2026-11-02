
import { useState } from "react";
import {
  LayoutDashboard,
  Database,
  BarChart3,
  Sparkles,
  BrainCircuit,
  FileSpreadsheet,
  Bell,
  Search,
  Upload,
  ArrowUpRight,
  TrendingUp,
  Users,
  Activity,
  ChevronDown,
  Menu,
  X,
  Zap,
  CalendarDays,
} from "lucide-react";


const navigation = [
  { name: "Dashboard", icon: LayoutDashboard },
  { name: "Data Explorer", icon: Database },
  { name: "Data Cleaning", icon: FileSpreadsheet },
  { name: "Visualizations", icon: BarChart3 },
  { name: "AI Assistant", icon: Sparkles },
  { name: "ML Analytics", icon: BrainCircuit },
];

const monthlyData = [
  45, 65, 55, 80, 60, 90, 70, 55, 85, 65, 95, 75,
];

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [uploadError, setUploadError] = useState("");
  const [monthlyAnalysis, setMonthlyAnalysis] = useState([]);
  const [salesInsightsError, setSalesInsightsError] = useState("");
  const maxMonthlySales = Math.max(
  ...monthlyAnalysis.map((item) => item.Daily_Sales),
  1
);

  // Calculate total missing values
  const totalMissingValues = uploadResult
    ? Object.values(uploadResult.missing_values).reduce(
        (total, count) => total + count,
        0
      )
    : 0;

  // Dynamic dashboard statistics
  const stats = [
    {
      title: "Total Records",
      value: uploadResult
        ? uploadResult.total_rows.toLocaleString("en-IN")
        : "—",
      change: uploadResult ? "Uploaded dataset" : "Upload a dataset",
      icon: Database,
    },
    {
      title: "Total Columns",
      value: uploadResult
        ? uploadResult.total_columns.toLocaleString("en-IN")
        : "—",
      change: "Dataset structure",
      icon: Activity,
    },
    {
      title: "Duplicate Rows",
      value: uploadResult
        ? uploadResult.duplicate_rows.toLocaleString("en-IN")
        : "—",
      change: "Exact duplicate records",
      icon: Users,
    },
    {
      title: "Missing Values",
      value: uploadResult
        ? totalMissingValues.toLocaleString("en-IN")
        : "—",
      change: "Total missing cells",
      icon: TrendingUp,
    },
  ];

  // Dataset upload handler
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    setUploading(true);
    setUploadError("");
    setSalesInsightsError("");
    setUploadResult(null);
    setMonthlyAnalysis([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Step 1: Upload dataset
      const response = await fetch(
        "http://127.0.0.1:8000/upload-dataset",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Dataset upload failed.");
      }

      setUploadResult(data);

      // Step 2: Get monthly sales insights
      try {
        const salesResponse = await fetch(
          "http://127.0.0.1:8000/sales-insights",
          {
            method: "POST",
            body: formData,
          }
        );

        const salesData = await salesResponse.json();

        if (!salesResponse.ok) {
          throw new Error(
            salesData.detail || "Sales insights could not be generated."
          );
        }

        setMonthlyAnalysis(
          salesData.results?.monthly_analysis || []
        );

      } catch (error) {
        setSalesInsightsError(error.message);
      }

    } catch (error) {
      setUploadError(error.message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-64 flex-col bg-slate-950 text-white transition-transform duration-300 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        } lg:translate-x-0`}
      >
        <div className="flex h-20 items-center justify-between border-b border-white/10 px-6">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-blue-600 p-2">
              <BrainCircuit size={25} />
            </div>

            <div>
              <h1 className="text-xl font-bold tracking-wide">
                DENNY<span className="text-blue-400"> AI</span>
              </h1>
              <p className="text-xs text-slate-400">
                Intelligent Analytics
              </p>
            </div>
          </div>

          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden"
          >
            <X size={22} />
          </button>
        </div>

        <div className="px-4 py-7">
          <p className="mb-4 px-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
            Workspace
          </p>

          <nav className="space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              const active = activePage === item.name;

              return (
                <button
                  key={item.name}
                  onClick={() => {
                    setActivePage(item.name);
                    setSidebarOpen(false);
                  }}
                  className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                    active
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-900/40"
                      : "text-slate-400 hover:bg-white/10 hover:text-white"
                  }`}
                >
                  <Icon size={19} />
                  {item.name}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="mt-auto p-4">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="mb-3 flex items-center gap-2 text-blue-400">
              <Zap size={18} />
              <span className="text-sm font-semibold">AI Powered</span>
            </div>

            <p className="text-xs leading-5 text-slate-400">
              Turn your raw data into meaningful business insights.
            </p>

            <button
              onClick={() => setActivePage("AI Assistant")}
              className="mt-4 w-full rounded-lg bg-blue-600 py-2 text-sm font-semibold hover:bg-blue-500"
            >
              Explore AI
            </button>
          </div>

          <div className="mt-5 flex items-center gap-3 border-t border-white/10 pt-5">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-500 font-bold">
              DK
            </div>

            <div>
              <p className="text-sm font-semibold">Data Analyst</p>
              <p className="text-xs text-slate-500">
                Personal Workspace
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="min-h-screen lg:ml-64">

        {/* Header */}
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur-md md:px-8">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-lg p-2 hover:bg-slate-100 lg:hidden"
            >
              <Menu size={23} />
            </button>

            <div>
              <h2 className="text-lg font-bold text-slate-800">
                {activePage}
              </h2>
              <p className="hidden text-xs text-slate-500 sm:block">
                Welcome to your analytics workspace
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
              <Search size={17} className="text-slate-400" />
              <input
                placeholder="Search..."
                className="w-32 bg-transparent text-sm outline-none"
              />
            </div>

            <button className="relative rounded-xl border border-slate-200 p-2.5 hover:bg-slate-50">
              <Bell size={19} />
              <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500"></span>
            </button>

            <button className="hidden items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-sm sm:flex">
              <CalendarDays size={16} />
              Overview
              <ChevronDown size={15} />
            </button>
          </div>
        </header>

        {/* Dashboard Body */}
        <div className="mx-auto max-w-7xl space-y-7 p-5 md:p-8">

          {/* Welcome Section */}
          <section className="flex flex-col justify-between gap-5 md:flex-row md:items-center">
            <div>
              <p className="mb-2 text-sm font-medium text-blue-600">
                ANALYTICS OVERVIEW
              </p>

              <h1 className="text-2xl font-bold tracking-tight text-slate-900 md:text-3xl">
                Welcome to DENNY AI 👋
              </h1>

              <p className="mt-2 text-sm text-slate-500">
                Analyze your data. Discover insights. Make smarter decisions.
              </p>
            </div>

            <label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700">
              <Upload size={18} />
              {uploading ? "Uploading..." : "Upload Dataset"}

              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                className="hidden"
                onChange={handleFileUpload}
                disabled={uploading}
              />
            </label>
          </section>

          {/* Upload Error */}
          {uploadError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              Upload Error: {uploadError}
            </div>
          )}

          {/* Dataset Upload Result */}
          {uploadResult && (
            <section className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div>
                <h3 className="text-lg font-bold text-green-700">
                  Dataset Uploaded Successfully!
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  {uploadResult.filename}
                </p>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div className="rounded-xl bg-blue-50 p-4">
                  <p className="text-sm text-slate-500">Total Rows</p>
                  <h4 className="mt-2 text-2xl font-bold">
                    {uploadResult.total_rows}
                  </h4>
                </div>

                <div className="rounded-xl bg-indigo-50 p-4">
                  <p className="text-sm text-slate-500">Total Columns</p>
                  <h4 className="mt-2 text-2xl font-bold">
                    {uploadResult.total_columns}
                  </h4>
                </div>

                <div className="rounded-xl bg-purple-50 p-4">
                  <p className="text-sm text-slate-500">Duplicate Rows</p>
                  <h4 className="mt-2 text-2xl font-bold">
                    {uploadResult.duplicate_rows}
                  </h4>
                </div>
              </div>

              <div>
                <h4 className="mb-3 font-semibold">Dataset Preview</h4>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-100">
                      <tr>
                        {uploadResult.columns.map((column) => (
                          <th key={column} className="whitespace-nowrap p-3">
                            {column}
                          </th>
                        ))}
                      </tr>
                    </thead>

                    <tbody>
                      {uploadResult.preview.map((row, index) => (
                        <tr key={index} className="border-b border-slate-100">
                          {uploadResult.columns.map((column) => (
                            <td key={column} className="whitespace-nowrap p-3">
                              {row[column] === null
                                ? "—"
                                : String(row[column])}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div>
                <h4 className="mb-3 font-semibold">Missing Values</h4>

                <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
                  {Object.entries(uploadResult.missing_values).map(
                    ([column, count]) => (
                      <div
                        key={column}
                        className="rounded-lg bg-slate-50 p-3"
                      >
                        <p className="truncate text-xs text-slate-500">
                          {column}
                        </p>
                        <p className="mt-1 font-bold">{count}</p>
                      </div>
                    )
                  )}
                </div>
              </div>
            </section>
          )}

          {/* Dynamic Statistics Cards */}
          <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
            {stats.map((stat) => {
              const Icon = stat.icon;

              return (
                <div
                  key={stat.title}
                  className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                >
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-slate-500">
                      {stat.title}
                    </p>

                    <div className="rounded-xl bg-blue-50 p-3 text-blue-600">
                      <Icon size={21} />
                    </div>
                  </div>

                  <h3 className="mt-5 text-2xl font-bold text-slate-900">
                    {stat.value}
                  </h3>

                  <p className="mt-2 text-xs text-slate-500">
                    {stat.change}
                  </p>
                </div>
              );
            })}
          </section>

          {/* Chart and AI Insights */}
          <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
            {uploadResult && (
              <>
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900">Revenue Overview</h3>
                      <p className="mt-1 text-xs text-slate-500">
                        Sample monthly revenue visualization
                      </p>
                    </div>

                    <button className="rounded-lg border border-slate-200 px-3 py-2 text-xs font-medium">
                      Monthly
                    </button>
                  </div>

                  <div className="mt-8 flex h-52 items-end justify-between gap-3 border-b border-l border-slate-200 px-2 pb-2">
                    {monthlyAnalysis.map((item, index) => (
                      <div
                        key={index}
                        style={{
                          height: `${(item.Daily_Sales / maxMonthlySales) * 100}%`,
                        }}
                        className="min-w-0 flex-1 rounded-t-md bg-blue-500 transition-all duration-300 hover:bg-blue-700"
                        title={`${item.Month_Name}: ₹${item.Daily_Sales.toLocaleString("en-IN", {
                          maximumFractionDigits: 2,
                        })}`}
                      ></div>
                    ))}
                  </div>

                  <div className="mt-3 flex justify-between text-xs text-slate-400">
                    {[
                      "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                    ].map((month) => (
                      <span key={month}>{month}</span>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl bg-gradient-to-br from-blue-700 to-indigo-900 p-6 text-white shadow-lg">
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-white/15 p-3">
                      <Sparkles size={23} />
                    </div>

                    <div>
                      <h3 className="font-bold">AI Insights</h3>
                      <p className="text-xs text-blue-200">Powered by Gemini AI</p>
                    </div>
                  </div>

                  <p className="mt-7 text-lg font-semibold">
                    Your data has a story. Let AI discover it.
                  </p>

                  <p className="mt-3 text-sm leading-6 text-blue-100">
                    Get intelligent analysis, identify patterns and discover business opportunities from your dataset.
                  </p>

                  <button
                    onClick={() => setActivePage("AI Assistant")}
                    className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-white py-3 text-sm font-bold text-blue-700 transition hover:bg-blue-50"
                  >
                    Explore AI Assistant
                    <ArrowUpRight size={17} />
                  </button>
                </div>
              </>
            )}
          </section>

          {/* Quick Actions */}
          <section>
            <div className="mb-5">
              <h3 className="text-lg font-bold text-slate-900">
                Explore Your Workspace
              </h3>
              <p className="mt-1 text-sm text-slate-500">
                Powerful tools to understand your data.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {[
                {
                  title: "Data Explorer",
                  description: "Inspect datasets and understand data structure.",
                  icon: Database,
                },
                {
                  title: "Data Visualization",
                  description: "Create meaningful charts and visual reports.",
                  icon: BarChart3,
                },
                {
                  title: "Machine Learning",
                  description: "Explore predictive models and evaluation.",
                  icon: BrainCircuit,
                },
              ].map((item) => {
                const Icon = item.icon;

                return (
                  <button
                    key={item.title}
                    onClick={() =>
                      setActivePage(
                        item.title === "Data Visualization"
                          ? "Visualizations"
                          : item.title === "Machine Learning"
                            ? "ML Analytics"
                            : item.title
                      )
                    }
                    className="rounded-2xl border border-slate-200 bg-white p-5 text-left shadow-sm transition hover:-translate-y-1 hover:border-blue-300 hover:shadow-md"
                  >
                    <div className="mb-4 inline-flex rounded-xl bg-blue-50 p-3 text-blue-600">
                      <Icon size={23} />
                    </div>

                    <h4 className="font-bold text-slate-900">
                      {item.title}
                    </h4>

                    <p className="mt-2 text-sm leading-6 text-slate-500">
                      {item.description}
                    </p>

                    <span className="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-blue-600">
                      Explore <ArrowUpRight size={15} />
                    </span>
                  </button>
                );
              })}
            </div>
          </section>

          {/* Footer */}
          <footer className="border-t border-slate-200 pt-6 text-center text-xs text-slate-400">
            © 2026 Denny AI. Intelligent Data Analysis Platform.
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
