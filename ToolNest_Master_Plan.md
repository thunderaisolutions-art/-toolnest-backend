# ToolNest.io — Complete Master Project Document

---

## BUSINESS OVERVIEW

- **Website:** ToolNest.io
- **Type:** Multi-tool SaaS platform
- **Target Users:** Designers, Developers, Writers, General users
- **Mission:** Every tool you need, in one place, for $2/month
- **Revenue Goal:** $3,000–$5,000/month by end of year
- **Monetization:** $2/month subscriptions + non-intrusive corner ads for free users

---

## PRICING PLANS

### Free Plan — $0/month
- Access to all 120+ tools
- Small non-intrusive corner ads (never full screen, never popups)
- Daily usage limits on heavy tools (video downloaders, converters)
- Google OAuth sign in

### Premium Plan — $2/month (shown as discounted from $4)
- Completely ad-free experience
- Unlimited usage on all tools
- Priority processing on heavy tools
- All future tools included automatically
- Google OAuth sign in + Stripe/PayPal payment

---

## UI DESIGN SYSTEM — ElevenLabs Inspired

### Design Philosophy
Clean, premium, minimal. Every element earns its place. No cheap AI tool vibes. No gradients, no rainbow colors, no clutter. White space is the design. Users should feel like they are using a $50/month product and be shocked it costs $2.

### Color Palette
- **Page Background:** #ffffff (pure white)
- **Section Accent:** #f5f5f5 (light gray — used for hero sections, tool input zones)
- **Primary Text:** #0a0a0a (near black — confident, premium)
- **Secondary Text:** #777777 (muted descriptions)
- **Hint Text:** #aaaaaa (placeholders, subtle labels)
- **Borders:** #ebebeb (ultra subtle — barely visible, everything breathes)
- **Hover Borders:** #d0d0d0 (slightly stronger on interaction)
- **Primary Button:** #0a0a0a background, #ffffff text
- **Ghost Button:** #ffffff background, #e0e0e0 border, #0a0a0a text
- **Badge Hot:** #fff0f0 background, #c0392b text
- **Badge Free:** #f0f0f0 background, #777 text

### Typography
- **Font:** Inter (Google Fonts — free)
- **H1 Hero:** 36–42px, font-weight 600, letter-spacing -1px, line-height 1.15
- **H2 Section:** 24px, font-weight 600, letter-spacing -0.5px
- **H3 Card Title:** 15px, font-weight 500
- **Body:** 14px, font-weight 400, line-height 1.6
- **Small/Labels:** 11–12px, font-weight 400 or 500
- **Nav Links:** 13px, font-weight 400

### Components

**Navigation Bar**
- Height: 56px
- Background: #ffffff
- Border bottom: 1px solid #ebebeb
- Logo: "ToolNest" — font-weight 600, "Nest" part slightly muted
- Nav links: Tools, Blog, Pricing
- Right side: Ghost "Sign in" button + Black "Go Premium — $2/mo" button

**Hero Section**
- Background: #f5f5f5
- Small badge above heading: "126 tools — one place — $2/month"
- H1: "Every tool you need. Nothing you don't."
- Subtext: short, punchy, speaks to the user's pain
- Centered search bar with magnifier icon — white background, subtle border

**Category Pills**
- Horizontal scrollable row
- Pill style: border-radius 20px, 6px 14px padding
- Active: #0a0a0a background, white text
- Inactive: white background, #e8e8e8 border, #555 text

**Tool Cards**
- Grid layout: 4 columns desktop, 2 tablet, 1 mobile
- Background: #ffffff
- Hover: #fafafa
- Separated by 1px #ebebeb lines (grid gap trick — no card shadows)
- Icon: 36x36px, #f5f5f5 background, 9px border radius
- Tool name: 13px, font-weight 500
- Description: 11px, #999
- Optional badge: Hot / Free / New

**Tool Page Layout**
- Background: #f5f5f5
- Inner card: #ffffff, border 1px #ebebeb, border-radius 12px
- Header: Tool name (18px 600) + subtitle description
- Body: Upload zone or input area
- Upload zone: dashed border, #fafafa background, centered icon + text
- Action buttons: Full width black primary + outline secondary

**Footer**
- Background: #0a0a0a (dark — strong contrast close)
- Logo in white
- Links: Privacy, Terms, Blog
- Right: "126 tools. One price."

---

## FULL INFRASTRUCTURE STACK

### Frontend
- **Platform:** WordPress (self-hosted on Hostinger VPS)
- **Theme:** Custom powerful theme — built from scratch, not a template
- **Local Dev:** WP Local (test everything locally before pushing live)
- **Each Tool:** Separate WordPress page template (tool-youtube-downloader.php, tool-json-formatter.php etc)
- **SEO Plugin:** RankMath or Yoast SEO
- **Auth Plugin:** Nextend Social Login (Google OAuth)
- **Payment:** WooCommerce + Stripe or PayPal

### Hosting
- **Provider:** Hostinger VPS
- **RAM:** 8GB
- **CPU:** 2 Cores
- **Disk:** 100GB
- **Bandwidth:** 8TB/month
- **Web Server:** Nginx
- **WordPress runs on:** Port 80/443

### Python Backend (Heavy Tools Only)
- **Platform:** Railway.app — Free tier at launch
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Deploy Method:** GitHub repo connected to Railway — push to GitHub = auto deploy
- **Upgrade Plan:** Upgrade Railway to $10/month after hitting 20 paying subscribers

### GitHub Repo Structure
```
toolnest-io/
├── /backend
│   ├── main.py               (FastAPI entry point)
│   ├── requirements.txt      (Railway reads this to install deps)
│   ├── downloader.py         (yt-dlp logic)
│   ├── converter.py          (FFmpeg logic)
│   ├── bgremover.py          (rembg logic — Phase 2)
│   ├── vectorizer.py         (VTracer logic — Phase 2)
│   └── pdftools.py           (PyMuPDF logic — Phase 2)
├── /wordpress-theme
│   ├── style.css
│   ├── functions.php
│   ├── header.php
│   ├── footer.php
│   ├── page-home.php
│   ├── page-tools.php
│   ├── page-blog.php
│   └── /tool-templates
│       ├── tool-yt-downloader.php
│       ├── tool-json-formatter.php
│       └── (one file per tool)
└── README.md
```

### Open Source Libraries Used
| Library | Purpose | Cost |
|---|---|---|
| yt-dlp | All video downloaders + 1800 sites | Free |
| FFmpeg | Video/audio conversion, compression | Free |
| rembg (danielgatis) | AI background remover — Phase 2 | Free |
| VTracer (visioncortex) | Image to SVG vectorizer — Phase 2 | Free |
| Potrace | Logo vectorizer — Phase 2 | Free |
| PyMuPDF | Entire PDF suite — Phase 2 | Free |
| Tesseract.js | OCR image to text — Phase 2 | Free |

### Monthly Cost at Launch
| Item | Cost |
|---|---|
| Hostinger VPS | ~$10/month |
| Railway (free tier) | $0 |
| All APIs | $0 |
| All libraries | $0 |
| **Total** | **~$10/month** |

Break even: 5 subscribers at $2/month.

---

## PHASE ROADMAP

### Phase 1 — Launch (Now, $0 backend cost)
- 120+ tools live
- Railway free tier for yt-dlp + FFmpeg
- All JS tools run in browser — zero server cost
- SEO + Blog starts immediately
- Google OAuth login
- Ads on free users

### Phase 2 — At 20 Subscribers (~$40/month revenue)
- Upgrade Railway to $10/month
- Add PDF Suite (PyMuPDF): 13 tools
- Add AI Background Remover (rembg)
- Add Vectorizer (VTracer + Potrace)
- Total tools: 142+

### Phase 3 — Empire ($500+/month revenue)
- Launch AIToolNest.io
- Launch DevNest.io
- Launch DesignNest.io
- All domains cross-promote each other
- Network effect — one visit leads to all domains

---

## SEO & BLOG STRATEGY

### Goal
150 blog posts in 5 months. Daily publishing. Every tool gets its own blog ecosystem.

### Blog Post Types
1. **How-To Posts** — "How to download YouTube videos in 4K for free"
2. **Vs/Comparison Posts** — "ToolNest vs iLovePDF — Which is better in 2025?"
3. **Best-Of Posts** — "Best free online tools for designers in 2025"
4. **Why Posts** — "Why every developer needs a JSON formatter"
5. **Complete Guides** — "Complete guide to image compression for web"

### SEO Tools (All Free)
- Google Search Console
- Google Analytics
- RankMath WordPress Plugin
- Ubersuggest (free tier)
- Answer The Public

### Internal Linking Strategy
- Every blog post links to the relevant tool page
- Every tool page links to its blog posts
- Related tools link to each other
- Creates a web Google loves to crawl

### Expected Timeline
- Month 1-2: Google crawling, minimal rankings
- Month 3-4: First page 2-3 rankings appear
- Month 4-5: Page 1 rankings for long-tail keywords
- Month 5+: Compounding traffic, daily new visitors

---

## REVENUE PROJECTIONS

| Milestone | Subscribers | Ad Revenue | Total/Month |
|---|---|---|---|
| Month 1-2 | 5-20 | $2-5 | $10-45 |
| Month 3-4 | 20-80 | $15-40 | $55-200 |
| Month 5-6 | 80-300 | $50-150 | $210-750 |
| Month 9-12 | 500-1500 | $200-500 | $1,200-3,500 |
| End of Year | 1000-2000 | $300-800 | $3,000-5,000 |

---

## COMPLETE TOOL LIST — 126 TOOLS AT LAUNCH

---

### CATEGORY 1: VIDEO & AUDIO TOOLS
*(Railway — yt-dlp + FFmpeg — Free tier)*

1. **YouTube Video Downloader**
   - Tech: yt-dlp + FFmpeg
   - Description: Paste any YouTube URL, select quality (4K/1080p/720p/480p/360p), download instantly. No limits, no watermarks.
   - Backend: Railway API call

2. **YouTube MP3 Downloader**
   - Tech: yt-dlp + FFmpeg
   - Description: Extract audio from any YouTube video. Output: MP3 at 128kbps or 320kbps.
   - Backend: Railway API call

3. **TikTok Video Downloader**
   - Tech: yt-dlp
   - Description: Download TikTok videos without watermark. Paste URL, get clean video file.
   - Backend: Railway API call

4. **Instagram Video Downloader**
   - Tech: yt-dlp
   - Description: Download Instagram videos from any public post. Paste URL, download MP4.
   - Backend: Railway API call

5. **Instagram Reels Downloader**
   - Tech: yt-dlp
   - Description: Download Instagram Reels. Same as video downloader, optimized for Reels URLs.
   - Backend: Railway API call

6. **Facebook Video Downloader**
   - Tech: yt-dlp
   - Description: Download public Facebook videos. Supports SD and HD quality.
   - Backend: Railway API call

7. **Twitter/X Video Downloader**
   - Tech: yt-dlp
   - Description: Download videos from Twitter/X posts. Paste tweet URL, get MP4.
   - Backend: Railway API call

8. **MP4 to MP3 Converter**
   - Tech: FFmpeg
   - Description: Upload any MP4 file, extract audio, download as MP3. Choose bitrate 128/192/320kbps.
   - Backend: Railway API call

9. **MP3 to MP4 Converter**
   - Tech: FFmpeg
   - Description: Combine MP3 audio with a static image to create an MP4 video file.
   - Backend: Railway API call

10. **Video to GIF Converter**
    - Tech: FFmpeg
    - Description: Upload a video clip, convert to GIF. Set FPS and dimensions.
    - Backend: Railway API call

11. **Audio Format Converter**
    - Tech: FFmpeg
    - Description: Convert between MP3, WAV, OGG, AAC, FLAC, M4A formats.
    - Backend: Railway API call

12. **Video Compressor**
    - Tech: FFmpeg
    - Description: Upload a large video, compress it to a smaller file size. Choose compression level.
    - Backend: Railway API call

13. **Audio Compressor**
    - Tech: FFmpeg
    - Description: Reduce MP3/WAV file size while maintaining acceptable quality.
    - Backend: Railway API call

14. **Video Trimmer**
    - Tech: FFmpeg
    - Description: Upload video, set start and end time, download trimmed clip.
    - Backend: Railway API call

---

### CATEGORY 2: IMAGE TOOLS
*(Pure JavaScript + Canvas API — Runs in Browser — $0)*

15. **Image Cropper**
    - Tech: Cropper.js (open source JS library)
    - Description: Upload image, drag to select crop area, download cropped result. Supports aspect ratio lock.
    - Backend: None — runs in browser

16. **Image Resizer**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image, enter target width/height, download resized image. Maintains aspect ratio option.
    - Backend: None — runs in browser

17. **Image Compressor**
    - Tech: Canvas API + browser-image-compression.js
    - Description: Upload image, set quality percentage, download compressed version. Shows before/after file size.
    - Backend: None — runs in browser

18. **Image Format Converter**
    - Tech: Canvas API (Pure JS)
    - Description: Upload PNG/JPG/WebP/GIF, choose output format, download converted file.
    - Backend: None — runs in browser

19. **PNG to JPG Converter**
    - Tech: Canvas API (Pure JS)
    - Description: Upload PNG, convert to JPG with custom quality setting.
    - Backend: None — runs in browser

20. **JPG to PNG Converter**
    - Tech: Canvas API (Pure JS)
    - Description: Upload JPG, convert to PNG with transparency support.
    - Backend: None — runs in browser

21. **Image to Base64**
    - Tech: FileReader API (Pure JS)
    - Description: Upload image, get Base64 string output. Copy to clipboard instantly.
    - Backend: None — runs in browser

22. **Base64 to Image**
    - Tech: Canvas API (Pure JS)
    - Description: Paste Base64 string, preview image, download as PNG.
    - Backend: None — runs in browser

23. **Image Size Finder**
    - Tech: Canvas API (Pure JS)
    - Description: Upload any image, instantly see Width x Height in pixels, file size, format, aspect ratio.
    - Backend: None — runs in browser

24. **Favicon Generator**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image or enter text, generate favicon in all sizes (16x16, 32x32, 48x48, 64x64). Download as .ico or PNG.
    - Backend: None — runs in browser

25. **Color Picker from Image**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image, click anywhere on it, get HEX/RGB/HSL color value of that pixel.
    - Backend: None — runs in browser

26. **Image Flipper & Rotator**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image, flip horizontally/vertically or rotate 90/180/270 degrees. Download result.
    - Backend: None — runs in browser

27. **Image Grayscale Converter**
    - Tech: Canvas API (Pure JS)
    - Description: Upload any color image, convert to black and white/grayscale instantly.
    - Backend: None — runs in browser

28. **Image Watermark Adder**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image, add text or image watermark. Set position, opacity, font size.
    - Backend: None — runs in browser

29. **Meme Generator**
    - Tech: Canvas API (Pure JS)
    - Description: Upload image or choose template, add top and bottom text, download as PNG.
    - Backend: None — runs in browser

30. **Screenshot to PNG**
    - Tech: html2canvas.js (open source)
    - Description: Enter a URL or paste HTML, capture as PNG screenshot.
    - Backend: None — runs in browser

31. **Bulk Image Resizer**
    - Tech: Canvas API + JSZip (Pure JS)
    - Description: Upload multiple images at once, set target dimensions, download all as ZIP.
    - Backend: None — runs in browser

32. **Photo Filter Tool**
    - Tech: Canvas API (Pure JS)
    - Description: Upload photo, apply filters (brightness, contrast, saturation, blur, sepia, vintage). Download result.
    - Backend: None — runs in browser

---

### CATEGORY 3: DEVELOPER TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

33. **JSON Formatter & Validator**
    - Tech: Pure JS
    - Description: Paste raw JSON, format it with proper indentation, validate syntax. Shows errors with line numbers.
    - Backend: None

34. **JSON to CSV Converter**
    - Tech: Pure JS
    - Description: Paste JSON array, convert to CSV table. Download as .csv file.
    - Backend: None

35. **CSV to JSON Converter**
    - Tech: Pure JS
    - Description: Paste or upload CSV, convert to JSON array. Copy or download result.
    - Backend: None

36. **Base64 Encoder & Decoder**
    - Tech: Pure JS (atob/btoa)
    - Description: Enter text, encode to Base64 or decode from Base64. Instant results.
    - Backend: None

37. **URL Encoder & Decoder**
    - Tech: Pure JS (encodeURIComponent/decodeURIComponent)
    - Description: Paste URL or string, encode or decode it. One click copy.
    - Backend: None

38. **HTML Encoder & Decoder**
    - Tech: Pure JS
    - Description: Encode special characters to HTML entities or decode them back.
    - Backend: None

39. **HTML Formatter**
    - Tech: js-beautify (open source JS)
    - Description: Paste minified or messy HTML, format it with proper indentation and line breaks.
    - Backend: None

40. **HTML to Markdown Converter**
    - Tech: Turndown.js (open source)
    - Description: Paste HTML code, convert to clean Markdown format.
    - Backend: None

41. **Markdown to HTML Converter**
    - Tech: Marked.js (open source)
    - Description: Write or paste Markdown, see live HTML preview and get raw HTML output.
    - Backend: None

42. **Markdown Editor & Preview**
    - Tech: Marked.js + CodeMirror (open source)
    - Description: Split-screen Markdown editor with live preview. Download as HTML or MD file.
    - Backend: None

43. **Regex Tester**
    - Tech: Pure JS
    - Description: Enter regex pattern and test string, see all matches highlighted in real time. Explains flags.
    - Backend: None

44. **CSS Minifier**
    - Tech: Pure JS
    - Description: Paste CSS code, remove whitespace and comments, get minified output. Shows size reduction.
    - Backend: None

45. **JS Minifier**
    - Tech: Terser.js (open source)
    - Description: Paste JavaScript, minify and compress it. Shows original vs minified size.
    - Backend: None

46. **CSS Beautifier**
    - Tech: js-beautify (open source)
    - Description: Paste minified CSS, format it with proper indentation and spacing.
    - Backend: None

47. **JS Beautifier**
    - Tech: js-beautify (open source)
    - Description: Paste minified JS, format it into readable code with proper indentation.
    - Backend: None

48. **SQL Formatter**
    - Tech: sql-formatter.js (open source)
    - Description: Paste SQL query, format it with proper line breaks and indentation. Supports MySQL, PostgreSQL, SQLite.
    - Backend: None

49. **Code Diff Checker**
    - Tech: diff.js (open source)
    - Description: Paste two versions of code side by side, highlights all additions, deletions and changes.
    - Backend: None

50. **Hash Generator**
    - Tech: Pure JS (SubtleCrypto API)
    - Description: Enter text, generate MD5, SHA-1, SHA-256, SHA-512 hashes instantly.
    - Backend: None

51. **UUID Generator**
    - Tech: Pure JS (crypto.randomUUID)
    - Description: Generate UUID v4 (and v1) strings. Bulk generate multiple UUIDs at once.
    - Backend: None

52. **JWT Decoder**
    - Tech: Pure JS (atob)
    - Description: Paste any JWT token, decode and display header, payload, and signature separately.
    - Backend: None

53. **Cron Expression Generator**
    - Tech: Pure JS
    - Description: Visual cron builder — set minute, hour, day, month, weekday using dropdowns. See human-readable description.
    - Backend: None

54. **Unix Timestamp Converter**
    - Tech: Pure JS
    - Description: Convert Unix timestamp to human readable date and vice versa. Shows timezone info.
    - Backend: None

55. **IP Address Lookup**
    - Tech: Pure JS + ip-api.com (free tier)
    - Description: Enter IP address or detect user's own IP. Shows country, city, ISP, timezone.
    - Backend: None

56. **Color Converter (HEX/RGB/HSL)**
    - Tech: Pure JS
    - Description: Enter color in any format (HEX, RGB, HSL, RGBA), convert to all other formats instantly. Shows color preview.
    - Backend: None

57. **SVG Optimizer**
    - Tech: SVGO (open source — runs in browser via WASM)
    - Description: Paste or upload SVG code, remove unnecessary metadata and optimize file size.
    - Backend: None

58. **XML Formatter**
    - Tech: Pure JS
    - Description: Paste raw or minified XML, format it with proper indentation and structure.
    - Backend: None

59. **YAML Validator**
    - Tech: js-yaml (open source)
    - Description: Paste YAML content, validate syntax, convert to JSON. Shows errors clearly.
    - Backend: None

60. **User Agent Parser**
    - Tech: Pure JS (ua-parser.js)
    - Description: Enter any User Agent string, parse and display browser, OS, device type details.
    - Backend: None

---

### CATEGORY 4: CSS GENERATOR TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

61. **CSS Gradient Generator**
    - Tech: Pure JS
    - Description: Visual gradient builder. Choose colors, angle, type (linear/radial/conic). Copy CSS output instantly.
    - Backend: None

62. **Box Shadow Generator**
    - Tech: Pure JS
    - Description: Sliders for horizontal, vertical, blur, spread, color, opacity. Live preview, copy CSS.
    - Backend: None

63. **Border Radius Generator**
    - Tech: Pure JS
    - Description: Control all 4 corners individually or together. Live preview, copy CSS border-radius value.
    - Backend: None

64. **Flexbox Generator**
    - Tech: Pure JS
    - Description: Visual flexbox playground. Toggle all flex properties, see live layout, copy CSS.
    - Backend: None

65. **CSS Grid Generator**
    - Tech: Pure JS
    - Description: Define columns and rows visually, set gaps, copy complete grid CSS.
    - Backend: None

66. **Text Shadow Generator**
    - Tech: Pure JS
    - Description: Sliders for X, Y, blur, color. Live text preview, copy CSS text-shadow.
    - Backend: None

67. **Button Generator**
    - Tech: Pure JS
    - Description: Customize button text, background, border, radius, padding, hover state. Copy CSS + HTML.
    - Backend: None

68. **Glassmorphism Generator**
    - Tech: Pure JS
    - Description: Generate frosted glass CSS effect. Control blur, transparency, border. Copy CSS.
    - Backend: None

69. **Neumorphism Generator**
    - Tech: Pure JS
    - Description: Generate soft UI neumorphic shadow CSS. Control size, radius, distance, blur, color, intensity.
    - Backend: None

70. **CSS Animation Generator**
    - Tech: Pure JS
    - Description: Choose animation type (fade, slide, bounce, spin etc), set duration/delay, copy @keyframes CSS.
    - Backend: None

71. **CSS Clip Path Generator**
    - Tech: Pure JS
    - Description: Drag points to create any clip-path shape visually. Copy CSS clip-path value.
    - Backend: None

---

### CATEGORY 5: TEXT TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

72. **Word Counter**
    - Tech: Pure JS
    - Description: Paste or type text, instantly see word count, character count, sentence count, paragraph count, reading time.
    - Backend: None

73. **Character Counter**
    - Tech: Pure JS
    - Description: Count characters with and without spaces. Useful for social media character limits (Twitter: 280, LinkedIn: 3000).
    - Backend: None

74. **Case Converter**
    - Tech: Pure JS
    - Description: Convert text to UPPERCASE, lowercase, Title Case, Sentence case, camelCase, snake_case, kebab-case.
    - Backend: None

75. **Text Diff Checker**
    - Tech: diff.js (open source)
    - Description: Two text boxes side by side. Highlights every addition and deletion between them in color.
    - Backend: None

76. **Lorem Ipsum Generator**
    - Tech: Pure JS
    - Description: Generate placeholder text. Choose number of words, sentences or paragraphs.
    - Backend: None

77. **Word Frequency Analyzer**
    - Tech: Pure JS
    - Description: Paste text, see all unique words ranked by frequency. Helps with SEO and readability.
    - Backend: None

78. **Readability Score Checker**
    - Tech: Pure JS
    - Description: Paste text, get Flesch Reading Ease score, Flesch-Kincaid Grade Level, and reading level label.
    - Backend: None

79. **Text to Binary**
    - Tech: Pure JS
    - Description: Type text, convert to binary (01001000 01100101 ...). One click copy.
    - Backend: None

80. **Binary to Text**
    - Tech: Pure JS
    - Description: Paste binary string, convert back to readable text.
    - Backend: None

81. **Text to Morse Code**
    - Tech: Pure JS
    - Description: Type text, convert to Morse code (dots and dashes). Optional audio playback.
    - Backend: None

82. **Morse Code to Text**
    - Tech: Pure JS
    - Description: Paste Morse code, decode it back to plain text.
    - Backend: None

83. **Duplicate Line Remover**
    - Tech: Pure JS
    - Description: Paste multi-line text, removes all duplicate lines. Option to sort alphabetically after.
    - Backend: None

84. **Text Sorter**
    - Tech: Pure JS
    - Description: Paste list of words or lines, sort alphabetically A-Z or Z-A. Numbers too.
    - Backend: None

85. **Reverse Text**
    - Tech: Pure JS
    - Description: Type text, reverse it character by character or word by word.
    - Backend: None

86. **Text Repeater**
    - Tech: Pure JS
    - Description: Enter text and a number, repeat text that many times. Set separator (comma, newline, space).
    - Backend: None

87. **Sentence Counter**
    - Tech: Pure JS
    - Description: Paste text, count total sentences. Also shows average words per sentence.
    - Backend: None

88. **Whitespace Remover**
    - Tech: Pure JS
    - Description: Remove leading/trailing spaces, double spaces, tabs. Clean messy text instantly.
    - Backend: None

89. **Text Encryptor**
    - Tech: Pure JS (SubtleCrypto AES)
    - Description: Enter text + password, encrypt to ciphertext. Decrypt with same password. Browser-only, nothing sent anywhere.
    - Backend: None

---

### CATEGORY 6: SEO & MARKETING TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

90. **Meta Tag Generator**
    - Tech: Pure JS
    - Description: Fill in title, description, keywords, author. Generates complete meta tag HTML. Preview how it looks on Google.
    - Backend: None

91. **Open Graph Tag Generator**
    - Tech: Pure JS
    - Description: Generate Facebook/LinkedIn Open Graph meta tags. Preview social share card appearance.
    - Backend: None

92. **Twitter Card Generator**
    - Tech: Pure JS
    - Description: Generate Twitter Card meta tags. Preview how link will appear when shared on Twitter/X.
    - Backend: None

93. **Robots.txt Generator**
    - Tech: Pure JS
    - Description: Visual builder for robots.txt file. Allow/disallow specific bots and paths. Download file.
    - Backend: None

94. **Sitemap XML Generator**
    - Tech: Pure JS
    - Description: Enter URLs with priority and change frequency, generate valid XML sitemap. Download .xml file.
    - Backend: None

95. **Slug & URL Generator**
    - Tech: Pure JS
    - Description: Enter any title or phrase, convert to clean URL slug (removes spaces, special chars, lowercase).
    - Backend: None

96. **Keyword Density Checker**
    - Tech: Pure JS
    - Description: Paste article text, enter target keyword, see density percentage and occurrences.
    - Backend: None

97. **UTM Link Builder**
    - Tech: Pure JS
    - Description: Enter URL + campaign source/medium/name/content, generate complete UTM tracking URL.
    - Backend: None

98. **Domain Age Checker**
    - Tech: Pure JS + WHOIS API (free tier)
    - Description: Enter any domain name, check when it was registered and how old it is.
    - Backend: None

---

### CATEGORY 7: CALCULATOR TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

99. **Age Calculator**
    - Tech: Pure JS
    - Description: Enter date of birth, get exact age in years, months, days, hours, minutes.
    - Backend: None

100. **Percentage Calculator**
     - Tech: Pure JS
     - Description: Multiple modes — X% of Y, X is what % of Y, percentage increase/decrease between two numbers.
     - Backend: None

101. **Unit Converter**
     - Tech: Pure JS
     - Description: Convert between Length, Weight, Temperature, Volume, Speed, Area, Data units. Comprehensive.
     - Backend: None

102. **Currency Converter**
     - Tech: Pure JS + exchangerate-api.com (free tier)
     - Description: Convert between 160+ currencies using live exchange rates.
     - Backend: None

103. **Aspect Ratio Calculator**
     - Tech: Pure JS
     - Description: Enter width and height, get aspect ratio (16:9, 4:3 etc). Or enter ratio + one dimension to get the other.
     - Backend: None

104. **Screen Resolution Checker**
     - Tech: Pure JS
     - Description: Instantly shows user's current screen resolution, viewport size, device pixel ratio, color depth.
     - Backend: None

105. **Color Contrast Checker (WCAG)**
     - Tech: Pure JS
     - Description: Enter foreground and background color, get contrast ratio, WCAG AA/AAA pass/fail result.
     - Backend: None

106. **Loan & EMI Calculator**
     - Tech: Pure JS
     - Description: Enter loan amount, interest rate, tenure. Get monthly EMI, total interest, total payment. Amortization table.
     - Backend: None

107. **BMI Calculator**
     - Tech: Pure JS
     - Description: Enter height and weight, get BMI score and category (Underweight/Normal/Overweight/Obese).
     - Backend: None

108. **Tip Calculator**
     - Tech: Pure JS
     - Description: Enter bill amount, tip percentage, number of people. Get tip amount and total per person.
     - Backend: None

109. **Discount Calculator**
     - Tech: Pure JS
     - Description: Enter original price and discount percentage, get sale price and savings amount.
     - Backend: None

110. **GPA Calculator**
     - Tech: Pure JS
     - Description: Add courses with grades and credit hours, calculate cumulative GPA. Supports 4.0 scale.
     - Backend: None

111. **Binary / Hex / Octal Converter**
     - Tech: Pure JS
     - Description: Enter number in any base (2, 8, 10, 16), instantly see converted value in all other bases.
     - Backend: None

---

### CATEGORY 8: MISCELLANEOUS TOOLS
*(Pure JavaScript — Runs in Browser — $0)*

112. **QR Code Generator**
     - Tech: qrcode.js (open source)
     - Description: Enter URL, text, email, phone or Wi-Fi credentials. Generate QR code, download as PNG or SVG.
     - Backend: None

113. **QR Code Reader**
     - Tech: jsQR (open source)
     - Description: Upload QR code image or use camera, decode and display the embedded content.
     - Backend: None

114. **Barcode Generator**
     - Tech: JsBarcode (open source)
     - Description: Enter data, choose barcode type (Code128, EAN, UPC, QR etc), download as PNG or SVG.
     - Backend: None

115. **Password Generator**
     - Tech: Pure JS (crypto.getRandomValues)
     - Description: Set length, toggle uppercase/lowercase/numbers/symbols. Generate cryptographically secure passwords.
     - Backend: None

116. **Password Strength Checker**
     - Tech: Pure JS
     - Description: Type password, see strength meter (Weak/Fair/Strong/Very Strong) with specific improvement tips.
     - Backend: None

117. **Random Number Generator**
     - Tech: Pure JS
     - Description: Set min and max range, generate single or multiple random numbers. Dice roller mode too.
     - Backend: None

118. **Invoice Generator**
     - Tech: Pure JS + jsPDF (open source)
     - Description: Fill in company details, client details, line items with quantities and prices. Generate professional PDF invoice.
     - Backend: None

119. **Pomodoro Timer**
     - Tech: Pure JS
     - Description: Classic 25-minute focus timer with 5-minute breaks. Customizable durations. Browser notification support.
     - Backend: None

120. **Color Palette Generator**
     - Tech: Pure JS
     - Description: Enter a base color or generate random palette. Get complementary, analogous, triadic color schemes with HEX codes.
     - Backend: None

121. **Gradient Palette Generator**
     - Tech: Pure JS
     - Description: Set two or more colors, generate a gradient palette with N steps between them. Copy all HEX codes.
     - Backend: None

122. **Email Validator**
     - Tech: Pure JS
     - Description: Enter email address, check if format is valid. Bulk validate multiple emails at once.
     - Backend: None

123. **Credit Card Validator**
     - Tech: Pure JS (Luhn algorithm)
     - Description: Enter card number, validate using Luhn algorithm, detect card type (Visa/Mastercard/Amex etc).
     - Backend: None

124. **Number to Words Converter**
     - Tech: Pure JS
     - Description: Enter any number (up to trillions), convert to English words. Useful for cheques, formal documents.
     - Backend: None

125. **Roman Numeral Converter**
     - Tech: Pure JS
     - Description: Convert between Arabic numbers (1, 2, 3) and Roman numerals (I, II, III). Works both directions.
     - Backend: None

126. **IBAN Validator**
     - Tech: Pure JS
     - Description: Enter IBAN number, validate format and checksum, display bank country and account details.
     - Backend: None

---

## PHASE 2 TOOLS (Unlock at 20 subscribers — Railway $10/month)

127. AI Background Remover — rembg (Python, Railway)
128. Image Vectorizer PNG to SVG — VTracer (Python, Railway)
129. Logo Vectorizer — Potrace (Python, Railway)
130. PDF to Word — PyMuPDF (Python, Railway)
131. Word to PDF — LibreOffice headless (Python, Railway)
132. PDF Merger — PyMuPDF (Python, Railway)
133. PDF Splitter — PyMuPDF (Python, Railway)
134. PDF Compressor — PyMuPDF + Ghostscript (Python, Railway)
135. PDF to Image — PyMuPDF (Python, Railway)
136. Image to PDF — PyMuPDF (Python, Railway)
137. PDF Page Remover — PyMuPDF (Python, Railway)
138. PDF Page Rotator — PyMuPDF (Python, Railway)
139. PDF to Text — PyMuPDF (Python, Railway)
140. PDF Password Protector — PyMuPDF (Python, Railway)
141. PDF Password Remover — PyMuPDF (Python, Railway)
142. PDF Watermark Adder — PyMuPDF (Python, Railway)

---

## NEXT STEPS — BUILD ORDER

1. Set up WordPress custom theme in WP Local
2. Create home page, tools listing page, individual tool page template
3. Build all Pure JS tools one by one (start with highest traffic — Image tools, Developer tools)
4. Set up Railway free tier + GitHub repo
5. Build FastAPI backend with yt-dlp + FFmpeg
6. Integrate video downloader tools with Railway API
7. Set up Google OAuth (Nextend Social Login plugin)
8. Set up Stripe payments + subscription logic
9. Push everything to Hostinger VPS
10. Set up RankMath SEO plugin + Google Search Console
11. Start daily blog posting
12. Launch ToolNest.io publicly
13. Monitor, optimize, grow

---

*InshAllah — ToolNest.io is going to be something extraordinary.*
