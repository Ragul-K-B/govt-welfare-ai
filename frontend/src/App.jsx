
import { useState } from 'react'
import governmentBanner from './assets/Welfare AI_ Empowering Citizens.png'
import './App.css'

const categories = [
  { name: 'Education', icon: '🎓', color: 'education' },
  { name: 'Agriculture', icon: '🌱', color: 'agriculture' },
  { name: 'Housing', icon: '🏠', color: 'housing' },
  { name: 'Women & Child Welfare', icon: '👩‍👧', color: 'women' },
  { name: 'Social Welfare', icon: '🤝', color: 'health' },
  { name: 'Marriage Assistance', icon: '💍', color: 'marriage' },
]

const navigationItems = [
  { name: 'Chat with Welfare AI', icon: '💬' },
  { name: 'Browse Schemes', icon: '🔎' },
  { name: 'Scheme Categories', icon: '▦' },
  { name: 'How It Works', icon: '📋' },
]

function App() {
  const [activeNav, setActiveNav] = useState('Chat with Welfare AI')
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)

  function sendMessage(text = message) {
    const trimmed = text.trim()
    if (!trimmed) return

    setMessages((previous) => [
      ...previous,
      { role: 'user', text: trimmed },
    ])

    setMessage('')
    setActiveNav('Chat with Welfare AI')
    setSelectedCategory(null)
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
              setActiveNav('Chat with Welfare AI')
              setMessage('How do I apply for a government welfare scheme?')
              setSelectedCategory(null)
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

        <main className="main-content">
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
                  <p>
                    Tell us about the assistance you are looking for.
                  </p>
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
          ) : activeNav === 'Browse Schemes' ||
            activeNav === 'Scheme Categories' ? (
            <section className="browse-content">
              <div className="chat-heading">
                <div>
                  <span className="eyebrow">EXPLORE WELFARE SUPPORT</span>
                  <h2>
                    {activeNav === 'Browse Schemes'
                      ? 'Browse Government Schemes'
                      : 'Explore Scheme Categories'}
                  </h2>
                  <p>
                    Choose a category to tell Welfare AI what kind of
                    assistance you need.
                  </p>
                </div>
                <div className="assistant-avatar">✦</div>
              </div>

              {activeNav === 'Browse Schemes' && (
                <input
                  className="browse-search"
                  type="search"
                  placeholder="Describe a scheme or the assistance you need..."
                  value={message}
                  onChange={(event) => setMessage(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter') sendMessage()
                  }}
                />
              )}

              {renderCategories()}
            </section>
          ) : (
            <>
              <div className="chat-heading">
                <div>
                  <span className="eyebrow">YOUR WELFARE COMPANION</span>
                  <h2>Discover Government Schemes</h2>
                  <p>
                    Tell us what assistance you need. We will help you
                    explore relevant government welfare schemes across India.
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
                <div className="conversation" aria-live="polite">
                  {messages.map((item, index) => (
                    <div
                      className="message-row user-row"
                      key={`${index}-${item.text}`}
                    >
                      <div className="message user-message">{item.text}</div>
                      <div className="user-avatar" aria-hidden="true">
                        👤
                      </div>
                    </div>
                  ))}

                  <div className="message-row assistant-row">
                    <div className="bot-avatar" aria-hidden="true">
                      ✦
                    </div>
                    <div className="message assistant-message">
                      Your message has been added to this conversation.
                      Connect this interface to the Welfare AI backend to
                      retrieve schemes, assess eligibility and ask
                      follow-up questions.
                    </div>
                  </div>
                </div>
              )}

              {selectedCategory && (
                <div className="suggestion-list">
                  <button
                    className="suggestion-chip"
                    type="button"
                    onClick={() => sendMessage(message)}
                  >
                    Explore {selectedCategory} schemes →
                  </button>

                  <button
                    className="suggestion-chip"
                    type="button"
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
                  placeholder="Describe your situation or ask a question..."
                />

                <button
                  className="send-button"
                  type="submit"
                  aria-label="Send message"
                  disabled={!message.trim()}
                >
                  ➤
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
              <span>💬</span>
              <h3>How can we help?</h3>
            </div>

            <div className="help-content">
              <p>Tell us what you need assistance with.</p>

              <button
                className="help-example"
                type="button"
                onClick={() => chooseCategory('Education')}
              >
                <span>🎓</span>
                <span>Education and scholarships</span>
              </button>

              <button
                className="help-example"
                type="button"
                onClick={() => chooseCategory('Agriculture')}
              >
                <span>🌾</span>
                <span>Farmer assistance</span>
              </button>

              <button
                className="help-example"
                type="button"
                onClick={() => chooseCategory('Housing')}
              >
                <span>🏠</span>
                <span>Housing support</span>
              </button>

              <button
                className="help-example"
                type="button"
                onClick={() => chooseCategory('Women & Child Welfare')}
              >
                <span>👩‍👧</span>
                <span>Women and child welfare</span>
              </button>
            </div>
          </section>

          <section className="categories-panel">
            <div className="panel-heading green-heading">
              <span>✿</span>
              <h3>Popular Categories</h3>
            </div>
            {renderCategories()}
          </section>

          <section className="need-help-panel">
            <div className="help-title">
              <span className="help-question">?</span>
              <h3>Need Help?</h3>
            </div>
            <p>
              Ask about scheme eligibility, benefits, required documents or
              application procedures.
            </p>
            <button
              className="help-link"
              type="button"
              onClick={() => {
                setActiveNav('Chat with Welfare AI')
                setSelectedCategory(null)
                setMessage('How do I apply for a government welfare scheme?')
              }}
            >
              Ask Welfare AI →
            </button>
          </section>
        </aside>
      </div>
    </div>
  )
}

export default App
