import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [lyrics, setLyrics] = useState('');
  const [parsedText, setParsedText] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPinyin, setShowPinyin] = useState(true);

  const handleTranslate = async () => {
    if (!lyrics.trim()) {
      setError('Please enter some Chinese text to translate');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/translate', { lyrics });
      console.log('API response:', response.data);
      
      // Use the API response to create React components
      const translation = response.data.translation;
      
      // Create an array of React components and strings for each line
      const formattedTranslation = [];
      
      // Process the API response data into React components
      translation.forEach(line => {
        const lineComponents = [];
        const pinyinComponents = [];
        
        if (Array.isArray(line)) {
          line.forEach(item => {
            if (typeof item === 'string') {
              lineComponents.push(item);
              pinyinComponents.push(' '.repeat(item.length));
            } else if (Array.isArray(item) && item.length === 3) {
              // It's a tuple of (chinese, pinyin, english)
              const [chinese, pinyin, english] = item;
              lineComponents.push(
                <ChineseTooltip 
                  key={`${chinese}-${lineComponents.length}`} 
                  chinese={chinese} 
                  pinyin={pinyin} 
                  english={english} 
                />
              );
              pinyinComponents.push(pinyin);
            }
          });
        } else {
          lineComponents.push(line);
          pinyinComponents.push('');
        }
        
        if (lineComponents.length > 0) {
          formattedTranslation.push({
            text: lineComponents,
            pinyin: pinyinComponents
          });
        }
      });
      
      setParsedText(formattedTranslation);
    } catch (err) {
      console.error('Translation error:', err);
      setError(err.response?.data?.error || 'An error occurred during translation');
    } finally {
      setLoading(false);
    }
  };

  // Function to parse Chinese text with pinyin and English
  const parseChineseText = (text) => {
    const segments = [];
    let i = 0;
    
    while (i < text.length) {
      const char = text[i];
      
      // Test if it's a Chinese character
      if (/[\u4e00-\u9fa5]/.test(char)) {
        // Find the end of the Chinese character (just one character)
        const chineseChar = char;
        i++;
        
        // Find the pinyin (all lowercase letters with possible tone marks)
        let pinyin = '';
        while (i < text.length && /[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]/.test(text[i])) {
          pinyin += text[i];
          i++;
        }
        
        // Find the English translation (all text until next Chinese character or end)
        let english = '';
        const startEnglish = i;
        
        while (i < text.length && !/[\u4e00-\u9fa5]/.test(text[i])) {
          english += text[i];
          i++;
        }
        
        // Add this segment with Chinese, pinyin, and English
        segments.push({
          type: 'chinese',
          chinese: chineseChar,
          pinyin: pinyin,
          english: english.trim()
        });
      } else {
        // Non-Chinese text, collect until we hit a Chinese character
        let text = '';
        while (i < text.length && !/[\u4e00-\u9fa5]/.test(text[i])) {
          text += text[i];
          i++;
        }
        
        if (text) {
          segments.push({
            type: 'text',
            content: text
          });
        } else {
          i++; // Safeguard to prevent infinite loop
        }
      }
    }
    
    return segments;
  };

  // New approach: create a simple component that shows Chinese with tooltips
  const ChineseTooltip = ({ chinese, pinyin, english }) => {
    return (
      <span className="tooltip-container">
        <span className="chinese-char">{chinese}</span>
        <span className="tooltip">
          <span className="tooltip-pinyin">{pinyin}</span>
          <span className="tooltip-english">{english}</span>
        </span>
      </span>
    );
  };

  // Function to show the example without changing the input text
  const handleExampleFormat = () => {
    // Multi-line example
    const directExample = [
      {
        text: [
          <ChineseTooltip key="1.1" chinese="给" pinyin="gěi" english="to supply" />,
          <ChineseTooltip key="1.2" chinese="你" pinyin="nǐ" english="you (informal, as opposed to courteous 您[nin2])" />,
          " ",
          <ChineseTooltip key="1.3" chinese="一" pinyin="yī" english="one" />,
          <ChineseTooltip key="1.4" chinese="张" pinyin="zhāng" english="to open up" />,
          " CD"
        ],
        pinyin: ["gěi", "nǐ", " ", "yī", "zhāng", " CD"]
      },
      {
        text: [
          <ChineseTooltip key="2.1" chinese="过" pinyin="guò" english="(experienced action marker)" />,
          <ChineseTooltip key="2.2" chinese="去" pinyin="qù" english="to go" />,
          " ",
          <ChineseTooltip key="2.3" chinese="的" pinyin="de" english="aim" />
        ],
        pinyin: ["guò", "qù", " ", "de"]
      }
    ];
    
    setParsedText(directExample);
  };

  // Toggle pinyin display
  const togglePinyin = () => {
    setShowPinyin(!showPinyin);
  };

  return (
    <div className="container">
      <h1>LYrcle - Chinese Lyrics Translator</h1>
      
      <div className="translation-container">
        <div className="input-section">
          <h2>Enter Chinese Lyrics</h2>
          <textarea
            value={lyrics}
            onChange={(e) => setLyrics(e.target.value)}
            placeholder="Enter Chinese lyrics here (one line per line)..."
          />
          <div className="button-group">
            <button onClick={handleTranslate} disabled={loading}>
              {loading ? 'Translating...' : 'Translate'}
            </button>
            <button onClick={handleExampleFormat} className="example-button">
              Show Example
            </button>
            <button onClick={togglePinyin} className="pinyin-toggle-button">
              {showPinyin ? 'Hide Pinyin' : 'Show Pinyin'}
            </button>
          </div>
        </div>
        
        {error && <div className="error">{error}</div>}
        
        {loading && <div className="loading">Translating your lyrics...</div>}
        
        {parsedText && (
          <div className="output-section">
            <h2>Translation</h2>
            <div className="translation-result">
              {parsedText.map((line, lineIndex) => (
                <div key={lineIndex} className="translation-group">
                  <div className="translation-line">
                    {line.text.map((item, index) => {
                      if (typeof item === 'string') {
                        return <span key={index}>{item}</span>;
                      }
                      return item; // Already a React component
                    })}
                    {lineIndex < parsedText.length - 1 && '\n'}
                  </div>
                  {showPinyin && (
                    <div className="pinyin-line">
                      {line.pinyin.map((p, index) => (
                        <span key={index} className="pinyin-text">{p}</span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App; 