import { Thermometer, Droplets, Power, Lightbulb, Fan, TrendingUp } from "lucide-react";
import { motion } from "motion/react";
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const temperatureData = [
  { time: "00:00", temp: 24, humidity: 65 },
  { time: "04:00", temp: 22, humidity: 70 },
  { time: "08:00", temp: 26, humidity: 60 },
  { time: "12:00", temp: 30, humidity: 55 },
  { time: "16:00", temp: 32, humidity: 50 },
  { time: "20:00", temp: 28, humidity: 58 },
  { time: "23:59", temp: 25, humidity: 63 },
];

const aiPredictionData = [
  { time: "Mon", value: 85 },
  { time: "Tue", value: 78 },
  { time: "Wed", value: 92 },
  { time: "Thu", value: 88 },
  { time: "Fri", value: 95 },
  { time: "Sat", value: 72 },
  { time: "Sun", value: 80 },
];

const rooms = [
  { name: "Living Room", temp: 26, humidity: 58, devices: 3, active: 2 },
  { name: "Bedroom", temp: 24, humidity: 62, devices: 2, active: 1 },
  { name: "Kitchen", temp: 28, humidity: 55, devices: 2, active: 2 },
];

export function Dashboard() {
  return (
    <div className="max-w-[1400px] mx-auto">
      {/* Header */}
      <div className="bg-white/60 backdrop-blur-xl rounded-3xl p-8 mb-6 border border-white/40 shadow-xl">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">Dashboard</h1>
        <p className="text-sm text-gray-500">Monitor your smart home environment</p>
      </div>

      {/* Active Devices Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-[#22d3ee] to-[#06b6d4] rounded-xl flex items-center justify-center">
              <Power className="w-6 h-6 text-white" />
            </div>
            <span className="text-xs font-semibold px-3 py-1 bg-green-100 text-green-700 rounded-full">Active</span>
          </div>
          <div className="text-3xl font-bold text-gray-800 mb-1">5/7</div>
          <div className="text-sm text-gray-500">Devices Running</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-[#6366f1] to-[#8b5cf6] rounded-xl flex items-center justify-center">
              <Lightbulb className="w-6 h-6 text-white" />
            </div>
            <span className="text-xs font-semibold px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full">On</span>
          </div>
          <div className="text-3xl font-bold text-gray-800 mb-1">3</div>
          <div className="text-sm text-gray-500">Lights On</div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-[#c084fc] to-[#a855f7] rounded-xl flex items-center justify-center">
              <Fan className="w-6 h-6 text-white" />
            </div>
            <span className="text-xs font-semibold px-3 py-1 bg-blue-100 text-blue-700 rounded-full">Running</span>
          </div>
          <div className="text-3xl font-bold text-gray-800 mb-1">2</div>
          <div className="text-sm text-gray-500">Fans Active</div>
        </motion.div>
      </div>

      {/* Temperature & Humidity Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg mb-6"
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold text-gray-800 mb-1">Temperature & Humidity</h2>
            <p className="text-sm text-gray-500">24-hour monitoring</p>
          </div>
          <div className="flex gap-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-[#6366f1] rounded-full"></div>
              <span className="text-sm text-gray-600">Temperature</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-[#22d3ee] rounded-full"></div>
              <span className="text-sm text-gray-600">Humidity</span>
            </div>
          </div>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={temperatureData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="time" stroke="#9ca3af" style={{ fontSize: '12px' }} />
            <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(99, 102, 241, 0.2)',
                borderRadius: '12px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Line type="monotone" dataKey="temp" stroke="#6366f1" strokeWidth={3} dot={{ r: 4 }} name="Temperature (°C)" />
            <Line type="monotone" dataKey="humidity" stroke="#22d3ee" strokeWidth={3} dot={{ r: 4 }} name="Humidity (%)" />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Room Statistics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-6">Rooms Overview</h2>
          <div className="space-y-4">
            {rooms.map((room) => (
              <div key={room.name} className="bg-gradient-to-br from-cyan-50 to-purple-50 rounded-xl p-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-bold text-gray-800">{room.name}</h3>
                  <span className="text-xs font-semibold px-2 py-1 bg-white/80 text-gray-600 rounded-lg">
                    {room.active}/{room.devices} Active
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="flex items-center gap-2">
                    <Thermometer className="w-4 h-4 text-[#6366f1]" />
                    <div>
                      <div className="text-xs text-gray-600">Temperature</div>
                      <div className="font-bold text-gray-800">{room.temp}°C</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Droplets className="w-4 h-4 text-[#22d3ee]" />
                    <div>
                      <div className="text-xs text-gray-600">Humidity</div>
                      <div className="font-bold text-gray-800">{room.humidity}%</div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* AI Prediction Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-white/40 shadow-lg"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-br from-[#6366f1] to-[#8b5cf6] rounded-xl flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-800">AI Prediction</h2>
              <p className="text-sm text-gray-500">Usage pattern analysis</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={aiPredictionData}>
              <defs>
                <linearGradient id="colorPrediction" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="time" stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <YAxis stroke="#9ca3af" style={{ fontSize: '12px' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(99, 102, 241, 0.2)',
                  borderRadius: '12px',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Area type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={3} fillOpacity={1} fill="url(#colorPrediction)" name="Efficiency Score" />
            </AreaChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-gradient-to-r from-cyan-50 to-purple-50 border border-[#6366f1]/20 rounded-xl">
            <p className="text-sm text-gray-700">
              <span className="font-semibold">AI Insight:</span> Your home efficiency is optimal on weekdays. Consider adjusting weekend schedules for better performance.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
