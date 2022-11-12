import type { VercelRequest, VercelResponse } from '@vercel/node'

export default async (req: VercelRequest, res: VercelResponse) => {
  const function_url = 'https://get-apartments-wmutchbu7q-uc.a.run.app'
  const url = `${function_url}?${req.query}`
  const data = await fetch(url)
  const json = await data.json()
  res.json(json)
}
