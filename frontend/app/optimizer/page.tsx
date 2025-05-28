"use client"

import type React from "react"
import type { NextApiRequest, NextApiResponse } from 'next'

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Route, FileText, ImageIcon, Download, AlertCircle, Loader2, ArrowLeft, Bus, Users } from "lucide-react"

// Define the result type for better type safety
interface RouteFile {
  csv_file: string
  csv_data: string
}

interface OptimizationResult {
  [key: string]: RouteFile
}

export default function OptimizerPage() {
  const [busFile, setBusFile] = useState<File | null>(null)
  const [studentFile, setStudentFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<OptimizationResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>, type: "bus" | "student") => {
    const file = event.target.files?.[0]
    if (!file) return

    if (type === "bus") {
      setBusFile(file)
    } else {
      setStudentFile(file)
    }
  }

  const handleSubmit = async () => {
    if (!busFile || !studentFile) {
      setError("Please upload both bus and student CSV files.")
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Create FormData to send files to the API
      const formData = new FormData()
      formData.append("busFile", busFile)
      formData.append("studentFile", studentFile)

      // Send the files to the Flask backend API
      const response = await fetch("http://localhost:5000/api/optimize_routes", {
      // const response = await fetch("/api/optimize_routes", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Failed to optimize routes")
      }

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error("Error optimizing routes:", error)
      setError(error instanceof Error ? error.message : "Error optimizing routes. Please try again.")
    }

    setLoading(false)
  }

  // Function to download a single file
  const handleDownload = (busIndex: string, fileType: "csv_file" | "html_file" | "png_file", fileName: string) => {
    if (!result) return

    const fileUrl = `http://localhost:5000/download/${result[busIndex][fileType]}`
    const link = document.createElement("a")
    link.href = fileUrl
    link.download = fileName
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // Function to download all files
  const handleDownloadAll = async () => {
    if (!result) return;

    console.log(result); // Debugging: Check the structure of the result object

    setLoading(true);

    try {
      for (const busIndex of Object.keys(result)) {
        const busNumber = Number.parseInt(busIndex);

        if (!result[busIndex]?.csv_file) {
          console.error(`Missing csv_file for busIndex: ${busIndex}`);
          continue; // Skip if csv_file is missing
        }

        handleDownload(busIndex, "csv_file", `bus_${busNumber}_route.csv`);
        await new Promise((resolve) => setTimeout(resolve, 300)); // Add a delay between downloads
      }
    } catch (error) {
      console.error("Error downloading files:", error);
      setError("Error downloading files. Please try again.");
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-800">
      {/* Header */}
      <header className="container mx-auto py-6 px-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Route className="h-8 w-8 text-white" />
          <span className="text-xl font-bold text-white">BusOptimize</span>
        </div>
        <Button asChild variant="ghost" className="text-white hover:bg-white/20">
          <Link href="/">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Home
          </Link>
        </Button>
      </header>

      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-white text-center mb-8">Bus Route Optimizer</h1>

        <div className="max-w-3xl mx-auto">
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white">Upload Your Data</CardTitle>
              <CardDescription className="text-white/70">
                Upload your bus and student data in CSV format to optimize routes
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {error && (
                <Alert variant="destructive" className="bg-red-500/20 border-red-500/50 text-white">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-4">
                <div>
                  <Label htmlFor="busFile" className="text-white mb-2 block">
                    Bus Data (CSV)
                  </Label>
                  <div className="flex items-center gap-4">
                    <Input
                      id="busFile"
                      type="file"
                      accept=".csv"
                      onChange={(e) => handleFileUpload(e, "bus")}
                      className="bg-white/20 border-white/30 text-white file:bg-indigo-600 file:text-white file:border-0"
                    />
                    <Bus className={`h-5 w-5 ${busFile ? "text-green-400" : "text-white/50"}`} />
                  </div>
                  {busFile && <p className="text-sm text-white/70 mt-1">File: {busFile.name}</p>}
                </div>

                <div>
                  <Label htmlFor="studentFile" className="text-white mb-2 block">
                    Student Data (CSV)
                  </Label>
                  <div className="flex items-center gap-4">
                    <Input
                      id="studentFile"
                      type="file"
                      accept=".csv"
                      onChange={(e) => handleFileUpload(e, "student")}
                      className="bg-white/20 border-white/30 text-white file:bg-indigo-600 file:text-white file:border-0"
                    />
                    <Users className={`h-5 w-5 ${studentFile ? "text-green-400" : "text-white/50"}`} />
                  </div>
                  {studentFile && <p className="text-sm text-white/70 mt-1">File: {studentFile.name}</p>}
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Button
                onClick={handleSubmit}
                disabled={loading || !busFile || !studentFile}
                className="w-full bg-indigo-600 hover:bg-indigo-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Optimizing Routes...
                  </>
                ) : (
                  <>
                    <Route className="mr-2 h-4 w-4" />
                    Optimize Routes
                  </>
                )}
              </Button>
            </CardFooter>
          </Card>

          {result && (
            <Card className="mt-8 bg-white/10 backdrop-blur-sm border-white/20">
              <CardHeader>
                <CardTitle className="text-white">Optimization Results</CardTitle>
                <CardDescription className="text-white/70">
                  Your optimized bus routes are ready to download
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="bus0" className="w-full">
                  <TabsList className="bg-white/20 w-full">
                    {Object.keys(result)
                      .filter((busIndex) => !isNaN(Number(busIndex))) // Filter out non-numeric keys
                      .sort((a, b) => Number(a) - Number(b)) // Sort busIndex in ascending order
                      .map((busIndex) => (
                        <TabsTrigger
                          key={busIndex}
                          value={`bus${busIndex}`}
                          className="text-white data-[state=active]:bg-indigo-600"
                        >
                          Bus {Number(busIndex)} {/* Correctly map bus index to tab */}
                        </TabsTrigger>
                      ))}
                    <TabsTrigger
                      value="summary"
                      className="text-white data-[state=active]:bg-indigo-600"
                    >
                      Summary
                    </TabsTrigger>
                  </TabsList>

                  {Object.keys(result)
                    .filter((busIndex) => !isNaN(Number(busIndex))) // Filter out non-numeric keys
                    .sort((a, b) => Number(a) - Number(b)) // Sort busIndex in ascending order
                    .map((busIndex) => (
                      <TabsContent key={busIndex} value={`bus${busIndex}`} className="mt-4">
                        <div className="grid gap-4">
                          <div className="flex items-center justify-between p-4 rounded-lg bg-white/5">
                            <div className="flex items-center">
                              <FileText className="h-5 w-5 text-white mr-3" />
                              <span className="text-white">Route Data (CSV)</span>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              className="bg-transparent border-white/30 text-white hover:bg-white/20"
                              onClick={() => handleDownload(busIndex, "csv_file", result[busIndex].csv_file)}
                            >
                              <Download className="h-4 w-4 mr-2" />
                              Download
                            </Button>
                          </div>
                        </div>
                      </TabsContent>
                    ))}
                  <TabsContent value="summary" className="mt-4">
                    <div className="text-white">
                      <h2 className="text-lg font-bold">Summary</h2>
                      <p>Summary of all bus routes is available for download below:</p>
                      <div className="flex items-center justify-between p-4 rounded-lg bg-white/5 mt-4">
                        <div className="flex items-center">
                          <FileText className="h-5 w-5 text-white mr-3" />
                          <span className="text-white">Bus Summary (CSV)</span>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          className="bg-transparent border-white/30 text-white hover:bg-white/20"
                          onClick={() => handleDownload("summary", "csv_file", "bus_summary.csv")}
                        >
                          <Download className="h-4 w-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
              <CardFooter>
                <Button
                  onClick={handleDownloadAll}
                  disabled={loading}
                  className="w-full bg-indigo-600 hover:bg-indigo-700"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Downloading...
                    </>
                  ) : (
                    <>
                      <Download className="mr-2 h-4 w-4" />
                      Download All Files
                    </>
                  )}
                </Button>
              </CardFooter>
            </Card>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-indigo-950 py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <p className="text-white/60">© {new Date().getFullYear()} BusOptimize. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' })
  }

  // Handle the file upload and optimization logic here
  // For example, you can parse the form data and process the files

  // Example response
  res.status(200).json({ result: 'Optimization result data' })
}

