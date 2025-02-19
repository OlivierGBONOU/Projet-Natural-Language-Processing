import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# A changer
artist = "Charles Aznavour"

# Configuration de la page
st.set_page_config(
    page_title= f"L'univers musical de {artist}",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger les données
@st.cache_data
def load_data():
    file_name = fr"{artist.strip().replace(' ', '_')}_sentiments.xlsx"
    # Lire le fichier Excel
    df = pd.read_excel(file_name)
    df = df[df['langue'] != "la"]
    return df

# Fonction pour créer le nuage de mots
@st.cache_data
def generate_wordcloud(text):
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        max_words=200,
        contour_width=3,
        contour_color='steelblue'
    ).generate(text)
    
    plt.figure(figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='white', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

# Chargement des données
df = load_data()

# Style CSS adapté pour un thème clair
st.markdown("""
    <style>
    .main {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    
    .css-1d391kg {
        background-color: #ffffff;
        padding: 1rem;
        border-right: 1px solid #ddd;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #333;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        color: #666;
    }
    
    div[data-testid="stMetricContainer"] {
        background: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 {
        color: #222;
    }
    
    .js-plotly-plot {
        margin: 1rem 0;
    }
    
    .stDataFrame {
        padding: 1rem 0;
    }

    /* Style pour la bannière */
    .banner {
        width: 100%;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Barre latérale optimisée
with st.sidebar:
    st.markdown(f"""
        <h1 style='text-align: center; color: black; font-size: 1.5rem; margin-bottom: 2rem;'>
            L'univers musical de {artist}
        </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: black; font-size: 1rem; margin-bottom: 1rem;'>Navigation</h3>", unsafe_allow_html=True)
    page = st.radio(
        f"{artist}'s Musical Universe",
        ["🏠 Accueil", "💭 Analyse des sentiments", "🌍 Analyse par langue", "☁️ Nuage de mots", "📜 Liste des chansons"],
        label_visibility="collapsed"
    )

# Contenu principal
if "🏠 Accueil" in page:
    # Ajout de la bannière
    st.markdown("""
        <div class="banner">
            <img src="https://yt3.googleusercontent.com/45sZFrmKIsw6-xyIXLYmzHl7zCZG2WogptAGlbz4CKJ1VUwXWfjVgoFFB0wZJIsSzWFhAruxRw=w1707-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj" style="width: 100%; height: auto;">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align: center;'>L'héritage musical de {artist}</h1>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total des chansons", len(df))
    with col2:
        st.metric("Chansons positives", len(df[df['sentiment'] == 'Positif']))
    with col3:
        st.metric("Chansons négatives", len(df[df['sentiment'] == 'Négatif']))
    with col4:
        st.metric("Score moyen", f"{df['score'].mean():.2f}")
    
    fig_pie = px.pie(
        df,
        names='sentiment',
        title='Répartition des sentiments',
        color_discrete_sequence=['#ff6f61', '#6b9ac4', '#88d498'],
        template="plotly_white",
        height=500
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

elif page == "💭 Analyse des sentiments":
    st.title("Analyse des sentiments")

    fig_scatter = px.scatter(
        df,
        x='score',
        y='sentiment',  # Remplacez par une colonne pertinente si nécessaire
        title='Distribution des scores de sentiment',
        color='sentiment',
        height=400
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    top_positive = df.nlargest(5, 'score')[['titre', 'score']]
    top_negative = df.nsmallest(5, 'score')[['titre', 'score']]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 des chansons les plus positives")
        st.dataframe(top_positive.style.format({"score": "{:.2f}"}))

    with col2:
        st.subheader("Top 5 des chansons les plus négatives")
        st.dataframe(top_negative.style.format({"score": "{:.2f}"}))

elif page == "🌍 Analyse par langue":
    st.title("Analyse par langue")
    
    lang_counts = df['langue'].value_counts()
    fig_bar = px.bar(
        x=lang_counts.index,
        y=lang_counts.values,
        title='Nombre de chansons par langue',
        labels={'x': 'Langue', 'y': 'Nombre'},
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    avg_score_by_lang = df.groupby('langue')['score'].mean().reset_index()
    fig_avg = px.bar(
        avg_score_by_lang,
        x='langue',
        y='score',
        title='Score moyen par langue',
        height=400
    )
    st.plotly_chart(fig_avg, use_container_width=True)
    
elif page == "☁️ Nuage de mots":
    st.title("Nuage de mots des paroles")
    
    # Filtre uniquement sur le sentiment
    sentiment_filter = st.selectbox(
        'Filtrer par sentiment',
        options=['Tous'] + sorted(df['sentiment'].unique())
    )
    
    # Filtrer les données
    if sentiment_filter == 'Tous':
        filtered_df = df
    else:
        filtered_df = df[df['sentiment'] == sentiment_filter]
    
    # Création du nuage de mots
    if not filtered_df.empty:
        all_lyrics = ' '.join(filtered_df['parole'].astype(str))
        wordcloud_image = generate_wordcloud(all_lyrics)
        st.image(wordcloud_image)
    else:
        st.warning("Aucune donnée disponible pour le filtre sélectionné.")

else:
    st.title("Liste complète des chansons")
    
    col1, col2 = st.columns(2)
    with col1:
        sentiment_filter = st.multiselect(
            'Filtrer par sentiment',
            options=sorted(df['sentiment'].unique()),
            default=df['sentiment'].unique()
        )
    with col2:
        langue_filter = st.multiselect(
            'Filtrer par langue',
            options=sorted(df['langue'].unique()),
            default=df['langue'].unique()
        )
    
    filtered_df = df[
        (df['sentiment'].isin(sentiment_filter)) &
        (df['langue'].isin(langue_filter))
    ]
    
    st.dataframe(
        filtered_df.sort_values('titre')[['titre', 'langue', 'score', 'sentiment']],
        height=500,
        use_container_width=True
    )