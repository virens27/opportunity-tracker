"use client";
import { useState, useEffect } from "react";

const API = "https://opportunity-tracker-cmqw.onrender.com";

interface Opportunity {
  id: number;
  title: string;
  organization: string;
  country: string;
  deadline: string;
  category: string;
  funding_amount: string;
  link: string;
  description: string;
  tags: string;
  women_friendly: boolean;
  indian_eligible: boolean;
  student_eligible: boolean;
  is_active: boolean;
}

const categoryColors: Record<string, string> = {
  Scholarship: "bg-blue-100 text-blue-800",
  Fellowship: "bg-purple-100 text-purple-800",
  Grant: "bg-green-100 text-green-800",
  Accelerator: "bg-orange-100 text-orange-800",
  Competition: "bg-red-100 text-red-800",
  Giveaway: "bg-yellow-100 text-yellow-800",
  Exchange: "bg-teal-100 text-teal-800",
  Other: "bg-gray-100 text-gray-800",
};

export default function Home() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [womenOnly, setWomenOnly] = useState(false);
  const [indianOnly, setIndianOnly] = useState(false);
  const [studentOnly, setStudentOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [tracked, setTracked] = useState<Record<number, string>>({});

  const fetchOpportunities = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (category) params.append("category", category);
      if (womenOnly) params.append("women_friendly", "true");
      if (indianOnly) params.append("indian_eligible", "true");
      if (studentOnly) params.append("student_eligible", "true");
      params.append("limit", "50");
      const res = await fetch(`${API}/opportunities?${params}`);
      const data = await res.json();
      setOpportunities(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchOpportunities();
  }, [womenOnly, indianOnly, studentOnly, category]);

  const handleTrack = async (id: number, status: string) => {
    try {
      await fetch(`${API}/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opportunity_id: id, status }),
      });
      setTracked((prev) => ({ ...prev, [id]: status }));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">🌍 Opportunity Tracker</h1>
              <p className="text-sm text-gray-500">AI-powered global opportunity discovery</p>
            </div>
            <span className="bg-green-100 text-green-800 text-xs font-medium px-3 py-1 rounded-full">
              {opportunities.length} opportunities
            </span>
          </div>
          <div className="flex gap-2 mb-3">
            <input
              type="text"
              placeholder="Search opportunities..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && fetchOpportunities()}
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={fetchOpportunities}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
              Search
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none">
              <option value="">All Categories</option>
              <option value="Scholarship">Scholarship</option>
              <option value="Fellowship">Fellowship</option>
              <option value="Grant">Grant</option>
              <option value="Accelerator">Accelerator</option>
              <option value="Competition">Competition</option>
              <option value="Giveaway">Giveaway</option>
              <option value="Exchange">Exchange</option>
            </select>
            {[
              { label: "🇮🇳 India Eligible", state: indianOnly, setter: setIndianOnly },
              { label: "👩 Women Friendly", state: womenOnly, setter: setWomenOnly },
              { label: "🎓 Students", state: studentOnly, setter: setStudentOnly },
            ].map(({ label, state, setter }) => (
              <button
                key={label}
                onClick={() => setter(!state)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors ${state ? "bg-blue-600 text-white border-blue-600" : "bg-white text-gray-600 border-gray-300 hover:bg-gray-50"}`}>
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        {loading ? (
          <div className="text-center py-20 text-gray-400">Loading opportunities...</div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-20 text-gray-400">No opportunities found.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {opportunities.map((opp) => (
              <div key={opp.id} className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow flex flex-col">
                <div className="flex flex-wrap gap-1.5 mb-3">
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${categoryColors[opp.category] || categoryColors.Other}`}>
                    {opp.category}
                  </span>
                  {opp.women_friendly && <span className="text-xs bg-pink-100 text-pink-800 px-2 py-0.5 rounded-full">👩 Women</span>}
                  {opp.indian_eligible && <span className="text-xs bg-orange-100 text-orange-800 px-2 py-0.5 rounded-full">🇮🇳 India</span>}
                  {opp.student_eligible && <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">🎓 Student</span>}
                </div>
                <h3 className="font-semibold text-gray-900 text-sm mb-1 line-clamp-2">{opp.title}</h3>
                <p className="text-xs text-gray-500 mb-2">{opp.organization} {opp.country ? `• ${opp.country}` : ""}</p>
                <p className="text-xs text-gray-600 line-clamp-3 mb-3 flex-1">{opp.description}</p>
                <div className="flex justify-between text-xs mb-3">
                  {opp.funding_amount && <span className="text-green-700 font-medium">💰 {opp.funding_amount}</span>}
                  {opp.deadline && <span className="text-red-600">⏰ {opp.deadline}</span>}
                </div>
                <div className="flex gap-2 mt-auto">
                  <a href={opp.link} target="_blank" rel="noopener noreferrer" className="flex-1 text-center bg-blue-600 text-white text-xs py-1.5 rounded-lg hover:bg-blue-700">
                    Apply
                  </a>
                  <select
                    value={tracked[opp.id] || ""}
                    onChange={(e) => handleTrack(opp.id, e.target.value)}
                    className="text-xs border border-gray-300 rounded-lg px-2 py-1.5 focus:outline-none">
                    <option value="">Track</option>
                    <option value="saved">💾 Saved</option>
                    <option value="planning">📋 Planning</option>
                    <option value="applied">✅ Applied</option>
                    <option value="interview">🎯 Interview</option>
                    <option value="accepted">🎉 Accepted</option>
                    <option value="rejected">❌ Rejected</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}