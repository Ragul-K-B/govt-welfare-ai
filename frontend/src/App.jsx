
import { useEffect, useRef, useState } from 'react'
import governmentBanner from './assets/Welfare AI_ Empowering Citizens.png'
import './App.css'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const categories = [
  { name: 'Education & Scholarships', icon: '🎓', color: 'education' },
  { name: 'Agriculture & Farmers', icon: '🌱', color: 'agriculture' },
  { name: 'Housing & Shelter', icon: '🏠', color: 'housing' },
  { name: 'Women & Child Welfare', icon: '👩‍👧', color: 'women' },
  { name: 'Social Welfare', icon: '👥', color: 'marriage' },
  { name: 'Health & Nutrition', icon: '♥', color: 'health' },
  { name: 'Skill Development', icon: '⚙', color: 'education' },
  { name: 'Employment Support', icon: '💼', color: 'agriculture' },
  { name: 'Disability Support', icon: '♿', color: 'housing' },
  { name: 'Senior Citizens', icon: '♟', color: 'women' },
]

const navigationItems = [
  { name: 'Chat with Welfare AI', icon: '💬' },
  { name: 'Browse Schemes', icon: '🔎' },
  { name: 'How It Works', icon: '📋' },
]

function formatValue(value) {
  if (value === null || value === undefined || value === '') {
    return ''
  }

  if (Array.isArray(value)) {
    return value
      .map((item) => formatValue(item))
      .filter(Boolean)
      .join(', ')
  }

  if (typeof value === 'object') {
    return Object.entries(value)
      .filter(([, item]) => item !== null && item !== undefined && item !== '')
      .map(([key, item]) => `${key.replace(/_/g, ' ')}: ${formatValue(item)}`)
      .join('; ')
  }

  return String(value)
}

function getSourceUrl(source) {
  if (!source || typeof source !== 'object') return ''

  const url = source.url || source.link || source.website

  if (typeof url !== 'string') return ''

  try {
    const parsedUrl = new URL(url)

    if (parsedUrl.protocol === 'https:' || parsedUrl.protocol === 'http:') {
      return parsedUrl.href
    }
  } catch {
    return ''
  }

  return ''
}

function SchemeCard({ scheme, uncertain = false, onViewDetails }) {
  const decision = String(scheme.decision || 'UNKNOWN').toUpperCase()
  const description = formatValue(scheme.description)
  const summary =
    description.length > 145 ? `${description.slice(0, 142).trimEnd()}…` : description
  const tags = [
    scheme.category,
    ...(Array.isArray(scheme.tags) ? scheme.tags : []),
  ].filter((tag) => typeof tag === 'string' && tag.trim()).slice(0, 3)

  return (
    <article className={`scheme-card ${uncertain ? 'scheme-card-uncertain' : 'scheme-card-eligible'}`}>
      <div className="scheme-card-icon" aria-hidden="true">▤</div>
      <div className="scheme-card-content">
        <div className="scheme-card-header">
          <div className="scheme-card-title">
            <h4>{scheme.name || 'Government welfare scheme'}</h4>
            <div className="scheme-meta">
              <span className="scheme-id">{scheme.scheme_id || 'Scheme ID unavailable'}</span>
              <span className="scheme-meta-divider">|</span>
              <span>{scheme.metadata?.government || scheme.metadata?.department || 'Government welfare scheme'}</span>
            </div>
          </div>
        </div>

        <p className="scheme-summary">
          {summary || 'Review the scheme details, eligibility criteria and application requirements.'}
        </p>

        {tags.length > 0 && (
          <div className="scheme-tags">
            {tags.map((tag) => <span key={tag}>{tag}</span>)}
          </div>
        )}
      </div>
      <div className="scheme-card-actions">
        <span
          className={`eligibility-badge ${uncertain ? 'unknown' : decision.toLowerCase()}`}
          title="Preliminary assessment based on the information currently available."
        >
          {uncertain ? 'Needs more information' : decision === 'PASS' ? '✓ Eligible match' : decision}
        </span>
        <button
          className="scheme-details-button"
          type="button"
          onClick={() => onViewDetails(scheme)}
        >
          View Scheme Details <span aria-hidden="true">→</span>
        </button>
      </div>
    </article>
  )
}

function detailEntries(value) {
  if (value === null || value === undefined || value === '') return []
  if (Array.isArray(value)) {
    return value.map((item) => formatValue(item)).filter(Boolean)
  }
  if (typeof value === 'object') {
    return Object.entries(value)
      .filter(([, item]) => item !== null && item !== undefined && item !== '')
      .map(([key, item]) => `${key.replace(/_/g, ' ')}: ${formatValue(item)}`)
  }
  return [String(value)]
}

function SchemeDetailsModal({ scheme, onClose }) {
  if (!scheme) return null

  const sections = [
    ['Description', scheme.description],
    ['Eligibility criteria', scheme.eligibility],
    ['Benefits', scheme.benefits],
    ['Required documents', scheme.documents],
    ['Application procedure', scheme.application],
    ['Additional information', scheme.metadata],
  ].filter(([, value]) => detailEntries(value).length > 0)

  const sources = Array.isArray(scheme.sources)
    ? scheme.sources
    : scheme.sources
      ? [scheme.sources]
      : []

  return (
    <div
      className="scheme-modal-backdrop"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <section
        className="scheme-details-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="scheme-details-title"
      >
        <header className="scheme-modal-header">
          <div>
            <span className="scheme-modal-eyebrow">GOVERNMENT WELFARE SCHEME</span>
            <h2 id="scheme-details-title">{scheme.name || 'Scheme details'}</h2>
            <p>{scheme.scheme_id || 'Scheme ID not available'}</p>
          </div>
          <button
            type="button"
            className="scheme-modal-close"
            onClick={onClose}
            aria-label="Close scheme details"
          >
            ×
          </button>
        </header>

        <div className="scheme-modal-content">
          {sections.map(([title, value]) => (
            <section className="scheme-detail-section" key={title}>
              <h3>{title}</h3>
              {detailEntries(value).length > 1 ? (
                <ul>
                  {detailEntries(value).map((entry, index) => (
                    <li key={`${title}-${index}`}>{entry}</li>
                  ))}
                </ul>
              ) : (
                <p>{detailEntries(value)[0]}</p>
              )}
            </section>
          ))}

          {sources.length > 0 && (
            <section className="scheme-detail-section">
              <h3>Official sources and links</h3>
              <ul className="scheme-source-list">
                {sources.map((source, index) => {
                  const url = getSourceUrl(source)
                  const label =
                    (source && typeof source === 'object' &&
                      (source.title || source.name || source.label)) ||
                    (url ? url : formatValue(source)) ||
                    `Source ${index + 1}`

                  return (
                    <li key={`source-${index}`}>
                      {url ? (
                        <a href={url} target="_blank" rel="noreferrer">
                          {label}
                        </a>
                      ) : (
                        <span>{label}</span>
                      )}
                    </li>
                  )
                })}
              </ul>
            </section>
          )}

          {sections.length === 0 && sources.length === 0 && (
            <p className="scheme-details-unavailable">
              Detailed scheme information is not available in the current result.
              Please verify the scheme through an official government source.
            </p>
          )}
          <p className="scheme-details-disclaimer">
            This is informational guidance, not official approval. Confirm current
            eligibility and application instructions with the responsible government department.
          </p>
        </div>
      </section>
    </div>
  )
}


const helpTopics = {
  profile: {
    title: 'Find schemes based on your profile',
    intro: 'Share only the details needed to find potentially relevant welfare schemes.',
    steps: [
      'Start in Chat with Welfare AI and describe the support you need.',
      'Mention relevant details such as your state, age, education or occupation, family income, and community category when applicable.',
      'Answer follow-up questions so the assistant can check the scheme rules against the information available.',
      'Open View Scheme Details to review benefits, eligibility, required documents, application steps and sources.',
    ],
    note: 'You can leave out details you are unsure about. Do not share Aadhaar numbers, bank details, passwords or other sensitive identification information.',
  },
  eligibility: {
    title: 'How eligibility checks work',
    intro: 'Welfare AI compares the information you provide with the eligibility rules stored for each scheme.',
    steps: [
      'Eligible / PASS means the available rules appear to match the details provided.',
      'Needs more information / UNKNOWN means one or more important details are missing or unclear.',
      'A scheme that does not match the available rules may not be shown as a potential match.',
      'Check the scheme details and confirm the latest requirements with the responsible government department before applying.',
    ],
    note: 'Results are preliminary guidance, not an official eligibility decision or guarantee of benefits.',
  },
  documents: {
    title: 'Understand required documents',
    intro: 'Document requirements differ between schemes and may change over time.',
    steps: [
      'Open a scheme card and select View Scheme Details.',
      'Review the Required documents section for the information currently available.',
      'Check whether originals, copies, certificates or online uploads are required with the official scheme authority.',
      'Prepare only the documents requested by the official application process.',
    ],
    note: 'If a document list is missing or unclear, verify it with the department or official portal. Do not upload documents into this chat.',
  },
  application: {
    title: 'Understand the application process',
    intro: 'Use the scheme details to identify the application route and verify the current process.',
    steps: [
      'Open View Scheme Details on the scheme you are interested in.',
      'Read the Application procedure section and follow any official source links provided.',
      'Confirm the application dates, eligibility conditions, required documents and submission method on the official portal or with the department.',
      'Keep any acknowledgement or reference number issued by the official application service.',
    ],
    note: 'Welfare AI does not submit applications or guarantee approval on your behalf.',
  },
  links: {
    title: 'Find and verify official links',
    intro: 'Official sources are the best place to confirm current scheme information.',
    steps: [
      'Open the relevant scheme details.',
      'Look for Official sources and links near the bottom of the details window.',
      'Check that the website belongs to the relevant government department or an official government portal.',
      'Verify the current rules, deadlines and application instructions before sharing information or applying.',
    ],
    note: 'If no source link is listed, search for the scheme on the relevant official government website rather than relying on an unofficial page.',
  },
  contact: {
    title: 'Contact and feedback',
    intro: 'Have a question, found a problem, or want to share feedback about Welfare AI? You can contact the project maintainer by email.',
    steps: [
      'For technical issues, describe what you were doing and include the exact error message and steps to reproduce the problem.',
      'If helpful, attach a screenshot that does not reveal personal or confidential information.',
      'For a scheme-specific decision or application, contact the department responsible for that scheme through its official government website.',
      'Never include Aadhaar numbers, bank details, passwords, OTPs or other sensitive personal information in your email.',
    ],
    note: 'Welfare AI provides preliminary guidance only. Scheme eligibility and application decisions must be confirmed with the responsible government department.',
  },
}

function HelpInfoModal({ topic, onClose }) {
  if (!topic) return null
  const content = helpTopics[topic] || helpTopics.profile

  return (
    <div
      className="help-modal-backdrop"
      role="presentation"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <section className="help-info-modal" role="dialog" aria-modal="true" aria-labelledby="help-info-title">
        <header className="help-info-header">
          <div className="help-info-icon" aria-hidden="true">ⓘ</div>
          <div>
            <span className="scheme-modal-eyebrow">WELFARE AI HELP CENTRE</span>
            <h2 id="help-info-title">{content.title}</h2>
          </div>
          <button type="button" className="scheme-modal-close" onClick={onClose} aria-label="Close help information">×</button>
        </header>
        <div className="help-info-content">
          <p>{content.intro}</p>
          {topic === 'contact' && (
            <div className="help-contact-card">
              <span className="help-contact-label">Email the project maintainer</span>
              <a className="help-contact-email" href="mailto:ragulkbcse@gmail.com">
                ragulkbcse@gmail.com
              </a>
              <span className="help-contact-hint">Select the email address to open your default email app.</span>
            </div>
          )}
          <ol>
            {content.steps.map((step, index) => <li key={`${topic}-${index}`}>{step}</li>)}
          </ol>
          <div className="help-info-note">
            <strong>Important</strong>
            <p>{content.note}</p>
          </div>
          <button className="primary-button help-info-done" type="button" onClick={onClose}>Got it</button>
        </div>
      </section>
    </div>
  )
}

function App() {
  const [activeNav, setActiveNav] = useState('Chat with Welfare AI')
  const [message, setMessage] = useState('')
  const [schemeSearch, setSchemeSearch] = useState('')
  const [schemeSearchResults, setSchemeSearchResults] = useState([])
  const [schemeSearchLoading, setSchemeSearchLoading] = useState(false)
  const [schemeSearchError, setSchemeSearchError] = useState('')
  const [messages, setMessages] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)

  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState('')
  const [citizenProfile, setCitizenProfile] = useState({})
  const [pendingQuestions, setPendingQuestions] = useState([])
  const [lastResult, setLastResult] = useState(null)
  const [activeSearch, setActiveSearch] = useState('')
  const [conversationContext, setConversationContext] = useState([])
  const [selectedSchemeDetails, setSelectedSchemeDetails] = useState(null)
  const [selectedHelpTopic, setSelectedHelpTopic] = useState(null)
  const conversationRef = useRef(null)
  const latestAssistantRef = useRef(null)

  // Start each new assistant response at its top instead of jumping to the bottom.
  useEffect(() => {
    if (messages.length === 0) return
    const lastMessage = messages[messages.length - 1]
    if (lastMessage?.role !== 'assistant') return

    const conversation = conversationRef.current
    const latestAssistant = latestAssistantRef.current
    if (!conversation || !latestAssistant) return

    const conversationTop = conversation.getBoundingClientRect().top
    const responseTop = latestAssistant.getBoundingClientRect().top
    conversation.scrollTo({
      top: Math.max(0, conversation.scrollTop + responseTop - conversationTop - 12),
      behavior: 'smooth',
    })
  }, [messages])

  // Search MongoDB schemes independently of the chatbot conversation.
  useEffect(() => {
    const searchText = schemeSearch.trim()

    if (!searchText) {
      setSchemeSearchResults([])
      setSchemeSearchError('')
      setSchemeSearchLoading(false)
      return undefined
    }

    const controller = new AbortController()
    const timeoutId = setTimeout(async () => {
      setSchemeSearchLoading(true)
      setSchemeSearchError('')

      try {
        const response = await fetch(
          `/api/schemes?search=${encodeURIComponent(searchText)}&limit=50`,
          { method: 'GET', signal: controller.signal },
        )
        const data = await response.json()

        if (!response.ok) {
          throw new Error(
            typeof data.detail === 'string'
              ? data.detail
              : 'Unable to search schemes. Please try again.',
          )
        }

        setSchemeSearchResults(Array.isArray(data.schemes) ? data.schemes : [])
      } catch (error) {
        if (error.name !== 'AbortError') {
          setSchemeSearchResults([])
          setSchemeSearchError(
            error instanceof Error ? error.message : 'Unable to search schemes.',
          )
        }
      } finally {
        if (!controller.signal.aborted) setSchemeSearchLoading(false)
      }
    }, 250)

    return () => {
      clearTimeout(timeoutId)
      controller.abort()
    }
  }, [schemeSearch])

  async function sendMessage(text = message) {
    const trimmed = text.trim()

    if (!trimmed || loading) return

    setMessages((previous) => [
      ...previous,
      { role: 'user', text: trimmed },
    ])

    setMessage('')
    setApiError('')
    setLoading(true)
    setActiveNav('Chat with Welfare AI')
    setSelectedCategory(null)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: trimmed,
          citizen_profile: citizenProfile,
          pending_questions: pendingQuestions,
          last_result: lastResult,
          active_search: activeSearch || null,
          conversation_context: conversationContext,
          top_k: 5,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : 'Unable to process your request. Please try again.',
        )
      }

      setCitizenProfile(data.profile ?? citizenProfile)
      setPendingQuestions(data.pending_questions ?? pendingQuestions)
      setLastResult(data.last_result ?? lastResult)
      setActiveSearch(data.active_search ?? activeSearch)
      setConversationContext(data.conversation_context ?? conversationContext)

      const result = data.result
      const resultSchemes = result?.schemes ?? []
      const requestedScheme = data.scheme_details?.scheme ?? null

      // A scheme-details intent returns its scheme separately from result.schemes.
      // Reuse the same scheme-card component so the user can open the existing modal.
      const displayedSchemes = requestedScheme ? [requestedScheme] : resultSchemes

      const passingSchemes = displayedSchemes.filter(
        (scheme) => String(scheme.decision || '').toUpperCase() === 'PASS',
      )
      const unknownCandidates = requestedScheme
        ? displayedSchemes.filter(
            (scheme) => String(scheme.decision || 'UNKNOWN').toUpperCase() === 'UNKNOWN',
          )
        : [
            ...(result?.uncertain_schemes ?? []),
            ...displayedSchemes.filter(
              (scheme) => String(scheme.decision || '').toUpperCase() === 'UNKNOWN',
            ),
          ].filter(
            (scheme) => String(scheme.decision || 'UNKNOWN').toUpperCase() === 'UNKNOWN',
          )
      const unknownSchemes = unknownCandidates.filter((scheme, index, all) => {
        const schemeKey = scheme.scheme_id || scheme.name
        return schemeKey
          ? all.findIndex(
              (candidate) => (candidate.scheme_id || candidate.name) === schemeKey,
            ) === index
          : all.indexOf(scheme) === index
      })

      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          text: data.answer || 'I could not generate a response.',
          schemes: passingSchemes,
          uncertainSchemes: unknownSchemes,
          questions: result?.followup_questions ?? [],
          noMatch: result?.no_match ?? false,
        },
      ])
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : 'Could not connect to Welfare AI. Check that the backend is running.',
      )
    } finally {
      setLoading(false)
    }
  }

  function requestSchemeDetails(scheme) {
    setSelectedSchemeDetails(scheme)
  }

  function chooseCategory(category) {
    setSelectedCategory(category)
    setActiveNav('Chat with Welfare AI')
    setMessage(
      `I am looking for government welfare schemes related to ${category}.`,
    )
  }

  function openChat() {
    setActiveNav('Chat with Welfare AI')
    setSelectedCategory(null)
  }

  function renderCategories() {
    return (
      <div className="category-grid">
        {categories.map((category) => (
          <button
            className={`category-card ${category.color}`}
            key={category.name}
            type="button"
            onClick={() => chooseCategory(category.name)}
          >
            <span className="category-icon">{category.icon}</span>
            <span className="category-label">{category.name}</span>
            <span className="category-arrow">↗</span>
          </button>
        ))}
      </div>
    )
  }

  function renderAssistantMessage(item, index) {
    const eligibleSchemes = item.schemes.filter(
      (scheme) => String(scheme.decision || '').toUpperCase() === 'PASS',
    )
    const unknownSchemes = [
      ...item.uncertainSchemes,
      ...item.schemes.filter(
        (scheme) => String(scheme.decision || '').toUpperCase() === 'UNKNOWN',
      ),
    ].filter((scheme, schemeIndex, all) =>
      all.findIndex((candidate) => candidate.scheme_id === scheme.scheme_id) === schemeIndex,
    )

    return (
      <div
        className="message-row assistant-row"
        key={`assistant-${index}`}
        ref={index === messages.length - 1 ? latestAssistantRef : null}
      >
        <div className="bot-avatar" aria-hidden="true">
          ✦
        </div>

        <div className="assistant-response">
          <div className="message assistant-message markdown-content">
  <ReactMarkdown remarkPlugins={[remarkGfm]}>
    {item.text || ''}
  </ReactMarkdown>
</div>

          {item.noMatch && (
            <p className="no-match-note">
              Try describing your situation in more detail or start a new
              search with a different assistance category.
            </p>
          )}

          {eligibleSchemes.length > 0 && (
            <section className="scheme-results eligible-results">
              <h3><span aria-hidden="true">✓</span> Schemes you appear eligible for ({eligibleSchemes.length})</h3>
              {eligibleSchemes.map((scheme, schemeIndex) => (
                <SchemeCard
                  key={scheme.scheme_id || `scheme-${schemeIndex}`}
                  scheme={scheme}
                  onViewDetails={requestSchemeDetails}
                />
              ))}
            </section>
          )}

          {unknownSchemes.length > 0 && (
            <section className="scheme-results uncertain-results">
              <h3><span aria-hidden="true">?</span> Schemes that may apply (need more information) ({unknownSchemes.length})</h3>
              <p className="results-note">
                More information or verification may be needed. These results
                are not confirmed eligibility decisions.
              </p>
              {unknownSchemes.map((scheme, schemeIndex) => (
                <SchemeCard
                  key={scheme.scheme_id || `uncertain-${schemeIndex}`}
                  scheme={scheme}
                  uncertain
                  onViewDetails={requestSchemeDetails}
                />
              ))}
            </section>
          )}

          {item.questions.length > 0 && (
            <section className="followup-section">
              <h3>A few more details</h3>
              <p>
                Please answer the relevant question or questions below. You can
                answer multiple questions in one message.
              </p>

              <ol className="followup-list">
                {item.questions.map((question, questionIndex) => (
                  <li key={`${question.attribute}-${questionIndex}`}>
                    {question.question}
                  </li>
                ))}
              </ol>
            </section>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <header className="top-header">
        <button
          className="banner-home"
          type="button"
          onClick={openChat}
          aria-label="Welfare AI home"
        >
          <img
            className="government-banner"
            src={governmentBanner}
            alt="Welfare AI — Your Guide to Government Welfare Schemes in India"
          />
        </button>

        <nav className="header-actions" aria-label="Header navigation">
          <button
            className={`header-button ${
              activeNav === 'How It Works' ? 'header-button-active' : ''
            }`}
            type="button"
            onClick={() => setActiveNav('How It Works')}
          >
            <span aria-hidden="true">ⓘ</span>
            <span>About</span>
          </button>

          <button
            className="header-button header-button-primary"
            type="button"
            onClick={() => {
              setSelectedHelpTopic('contact')
            }}
          >
            <span aria-hidden="true">✦</span>
            <span>Get Help</span>
          </button>
        </nav>
      </header>

      <div className="dashboard">
        <aside className="left-sidebar">
          <nav className="main-navigation" aria-label="Main navigation">
            {navigationItems.map((item) => (
              <button
                key={item.name}
                type="button"
                className={`nav-item ${
                  activeNav === item.name ? 'active' : ''
                }`}
                onClick={() => {
                  setActiveNav(item.name)
                  setSelectedCategory(null)
                }}
              >
                <span className="nav-icon">{item.icon}</span>
                <span>{item.name}</span>
              </button>
            ))}
          </nav>

          <div className="sidebar-category-list">
            <h3>Popular Categories</h3>
            {categories.map((category) => (
              <button
                key={category.name}
                type="button"
                className="sidebar-category"
                onClick={() => chooseCategory(category.name)}
              >
                <span aria-hidden="true">{category.icon}</span>
                <span>{category.name}</span>
              </button>
            ))}
          </div>

          <div className="sidebar-note">
            <div className="note-icon">🇮🇳</div>
            <h3>Welfare for Everyone</h3>
            <p>
              Discover government welfare schemes and understand their
              eligibility requirements in one place.
            </p>
          </div>

          <div className="sidebar-footer">
            <span className="status-dot" />
            <span>Welfare AI Assistant</span>
          </div>
        </aside>

        <main
          className={`main-content ${
            activeNav === 'Chat with Welfare AI' ? 'chat-main-content' : ''
          }`}
        >
          {activeNav === 'How It Works' ? (
            <section className="about-page">
              <span className="eyebrow">ABOUT WELFARE AI</span>
              <h2>Find support that fits your situation</h2>
              <p>
                Welfare AI helps you discover government welfare schemes
                based on the information you share.
              </p>

              <div className="info-steps">
                <article className="info-step">
                  <span className="info-step-number">01</span>
                  <h4>Describe your needs</h4>
                  <p>Tell us about the assistance you are looking for.</p>
                </article>

                <article className="info-step">
                  <span className="info-step-number">02</span>
                  <h4>Answer a few questions</h4>
                  <p>
                    Share relevant details so we can assess possible matches.
                  </p>
                </article>

                <article className="info-step">
                  <span className="info-step-number">03</span>
                  <h4>Explore schemes</h4>
                  <p>
                    Review potential schemes, benefits and eligibility
                    requirements.
                  </p>
                </article>

                <article className="info-step">
                  <span className="info-step-number">04</span>
                  <h4>Verify before applying</h4>
                  <p>
                    Check the official scheme information and application
                    instructions before submitting an application.
                  </p>
                </article>
              </div>

              <button
                className="primary-button"
                type="button"
                onClick={openChat}
              >
                Start discovering schemes →
              </button>
            </section>
          ) : activeNav === 'Browse Schemes' ? (
            <section className="browse-content">
              <div className="chat-heading">
                <div>
                  <span className="eyebrow">EXPLORE WELFARE SUPPORT</span>
                  <h2>
                    Browse Government Schemes
                  </h2>
                  <p>
                    Search government schemes by name and open a result to explore its benefits, eligibility and application details.
                  </p>
                </div>
                <div className="assistant-avatar">✦</div>
              </div>

              {activeNav === 'Browse Schemes' ? (
                <section className="browse-schemes-page">
                  <label className="browse-search-container">
                    <span className="browse-search-icon" aria-hidden="true">⌕</span>
                    <input
                      className="browse-search"
                      type="search"
                      value={schemeSearch}
                      onChange={(event) => setSchemeSearch(event.target.value)}
                      placeholder="Search by government scheme name..."
                      aria-label="Search government schemes by name"
                    />
                    {schemeSearch && (
                      <button
                        className="browse-search-clear"
                        type="button"
                        onClick={() => setSchemeSearch('')}
                        aria-label="Clear scheme search"
                      >
                        ×
                      </button>
                    )}
                  </label>

                  <p className="browse-search-hint">
                    Search the scheme database by name. Select a result to view its
                    benefits, eligibility criteria, documents and application details.
                  </p>

                  <div className="browse-scheme-results" aria-live="polite">
                    {!schemeSearch.trim() ? (
                      <div className="browse-empty-state">
                        <div className="browse-empty-icon" aria-hidden="true">⌕</div>
                        <h3>Find a scheme by name</h3>
                        <p>Start typing a scheme name above to see matching government schemes.</p>
                      </div>
                    ) : schemeSearchLoading ? (
                      <p className="browse-results-status">Searching schemes…</p>
                    ) : schemeSearchError ? (
                      <p className="browse-results-error" role="alert">{schemeSearchError}</p>
                    ) : schemeSearchResults.length === 0 ? (
                      <p className="browse-results-status">No matching schemes found. Try a different name.</p>
                    ) : (
                      <>
                        <h3 className="browse-results-heading">
                          {schemeSearchResults.length} matching scheme{schemeSearchResults.length === 1 ? '' : 's'}
                        </h3>
                        <div className="browse-scheme-grid">
                          {schemeSearchResults.map((scheme) => (
                            <button
                              type="button"
                              className="browse-scheme-result"
                              key={scheme.scheme_id || scheme.name}
                              onClick={() => requestSchemeDetails(scheme)}
                            >
                              <span className="browse-scheme-result-icon" aria-hidden="true">▤</span>
                              <span className="browse-scheme-result-content">
                                <strong>{scheme.name || 'Government welfare scheme'}</strong>
                                <span className="browse-scheme-id">{scheme.scheme_id || 'Scheme ID unavailable'}</span>
                                {scheme.description && (
                                  <span className="browse-scheme-description">
                                    {formatValue(scheme.description).slice(0, 180)}
                                    {formatValue(scheme.description).length > 180 ? '…' : ''}
                                  </span>
                                )}
                              </span>
                              <span className="browse-scheme-result-arrow" aria-hidden="true">→</span>
                            </button>
                          ))}
                        </div>
                      </>
                    )}
                  </div>
                </section>
              ) : (
                renderCategories()
              )}
            </section>
          ) : (
            <>
              <div className="chat-heading">
                <div>
                  <span className="eyebrow">YOUR WELFARE COMPANION</span>
                  <h2>Discover Government Schemes</h2>
                  <p>
                    Tell us what assistance you need. We will help you explore
                    relevant government welfare schemes across India.
                  </p>
                </div>
                <div className="assistant-avatar">✦</div>
              </div>

              {messages.length === 0 ? (
                <section className="category-browser">
                  <h3>What kind of assistance are you looking for?</h3>
                  <p>
                    Select a category or describe your situation below.
                  </p>
                  {renderCategories()}
                </section>
              ) : (
                <div className="conversation" aria-live="polite" ref={conversationRef}>
                  {messages.map((item, index) =>
                    item.role === 'user' ? (
                      <div
                        className="message-row user-row"
                        key={`user-${index}-${item.text}`}
                      >
                        <div className="message user-message">{item.text}</div>
                        <div className="user-avatar" aria-hidden="true">
                          👤
                        </div>
                      </div>
                    ) : (
                      renderAssistantMessage(item, index)
                    ),
                  )}

                  {loading && (
                    <div className="message-row assistant-row">
                      <div className="bot-avatar" aria-hidden="true">
                        ✦
                      </div>
                      <div
                        className="message assistant-message"
                        role="status"
                      >
                        Checking relevant welfare schemes…
                      </div>
                    </div>
                  )}
                </div>
              )}

              {apiError && (
                <div className="api-error" role="alert">
                  <strong>Unable to get a response</strong>
                  <p>{apiError}</p>
                  <p>
                    Check that the FastAPI server is running and try sending
                    your message again.
                  </p>
                </div>
              )}

              {selectedCategory && (
                <div className="suggestion-list">
                  <button
                    className="suggestion-chip"
                    type="button"
                    disabled={loading}
                    onClick={() => sendMessage(message)}
                  >
                    Explore {selectedCategory} schemes →
                  </button>

                  <button
                    className="suggestion-chip"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setSelectedCategory(null)
                      setMessage('')
                    }}
                  >
                    Choose another category
                  </button>
                </div>
              )}

              <form
                className="message-composer"
                onSubmit={(event) => {
                  event.preventDefault()
                  sendMessage()
                }}
              >
                <button
                  className="attachment-button"
                  type="button"
                  aria-label="Attachments unavailable"
                  title="Attachments are not available yet"
                  disabled
                >
                  📎
                </button>

                <input
                  aria-label="Your message"
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  placeholder={
                    pendingQuestions.length > 0
                      ? 'Answer the follow-up questions...'
                      : 'Describe your situation or ask a question...'
                  }
                  disabled={loading}
                />

                <button
                  className="send-button"
                  type="submit"
                  aria-label="Send message"
                  disabled={!message.trim() || loading}
                >
                  {loading ? '…' : '➤'}
                </button>
              </form>

              <p className="composer-note">
                Avoid sharing sensitive personal identification numbers.
              </p>
            </>
          )}
        </main>

        <aside className="right-sidebar">
          <section className="information-panel">
            <div className="panel-heading blue-heading">
              <span>ⓘ</span>
              <h3>How can we help?</h3>
            </div>
            <div className="help-content">
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('profile')}>
                <span>▦</span><span>Find schemes based on my profile</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('eligibility')}>
                <span>⚙</span><span>Check my eligibility</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('documents')}>
                <span>▤</span><span>Understand required documents</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('application')}>
                <span>▣</span><span>Get application process details</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('links')}>
                <span>↗</span><span>Find official links</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
              <button className="help-example" type="button" onClick={() => setSelectedHelpTopic('contact')}>
                <span>✉</span><span>Contact & feedback</span><span className="help-example-arrow" aria-hidden="true">›</span>
              </button>
            </div>
          </section>

          <section className="quick-examples-panel">
            <div className="panel-heading amber-heading">
              <span>☼</span>
              <h3>Quick Examples</h3>
            </div>
            {[
              'Scholarships for engineering students',
              'Schemes for farmers',
              'Housing schemes for low income families',
              'Financial assistance for women',
            ].map((example) => (
              <button
                key={example}
                className="help-example quick-example"
                type="button"
                onClick={() => sendMessage(example)}
              >
                <span>{example}</span><span aria-hidden="true">›</span>
              </button>
            ))}
          </section>

          <section className="need-help-panel">
            <div className="help-title">
              <span className="help-question">!</span>
              <h3>Important Note</h3>
            </div>
            <p>
              Welfare AI provides guidance based on available scheme information.
              Eligibility assessments are preliminary. Please verify current
              rules, deadlines and application details on official government
              websites before applying.
            </p>
          </section>
        </aside>
      </div>
      <SchemeDetailsModal
        scheme={selectedSchemeDetails}
        onClose={() => setSelectedSchemeDetails(null)}
      />
      <HelpInfoModal
        topic={selectedHelpTopic}
        onClose={() => setSelectedHelpTopic(null)}
      />
    </div>
  )
}

export default App
