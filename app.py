import streamlit as st
from utils.llm import analyze_prompt
from utils.image_gen import generate_image
from PIL import Image
import io
import random

st.markdown(
    """
<style>
    /* Main buttons */
    div.stButton > button {
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: 2px solid #FF4B4B;
        background-color: #FF4B4B;
        color: white;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.3);
    }
    
    div.stButton > button:focus {
        box-shadow: none;
        border-color: #FF4B4B;
    }
    
    /* Download button */
    div.stDownloadButton > button {
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: 2px solid #FF4B4B;
        background-color: transparent;
        color: #FF4B4B;
        transition: all 0.3s ease;
    }
    
    div.stDownloadButton > button:hover {
        background-color: #FF4B4B;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Radio buttons - 2 columns on desktop, 1 on mobile */
    div[role="radiogroup"] {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
    }
    
    @media (max-width: 768px) {
        div[role="radiogroup"] {
            grid-template-columns: 1fr;
        }
    }
    
    div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.75rem 1.25rem;
        border-radius: 20px;
        margin: 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 75, 75, 0.1);
        border-color: #FF4B4B;
        transform: translateX(5px);
    }
    
    /* Selected radio button */
    div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #FF4B4B;
        color: white;
        border-color: #FF4B4B;
    }
    /* Remove outer container styling */
    div[data-testid="stTextInput"] > div,
    div[data-testid="stTextInput"] > div > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        border-radius: 15px; /* Match the input border-radius */
    }
    
        /* Text inputs with border color wave */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 15px;
        padding: 0.75rem 1.25rem;
        border: 2px solid rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        animation: border-wave 2s ease-in-out infinite;
    }

    @keyframes border-wave {
        0%, 100% {
            border-color: rgba(255, 75, 75, 0.3);
        }
        50% {
            border-color: rgba(255, 75, 75, 1);
        }
    }

    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #FF4B4B;
        box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.3);
        background-color: transparent;
    }
    
    /* Category labels */
    .stMarkdown strong {
        color: #FF4B4B;
        font-size: 1.1em;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FF4B4B, transparent);
        margin: 2rem 0;
    }

    /* Add to existing CSS */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    div[data-testid="stMarkdown"] {
        animation: fadeIn 0.5s ease-in;
    }
    /* Hide input instructions */
    div[data-testid="InputInstructions"] {
    display: none !important;
    }
    
</style>
""",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.title("🎨 AI Image Generator")
    st.markdown("---")

    st.subheader("About")
    st.write(
        """
    Transform simple ideas into stunning, 
    detailed AI-generated images.
    """
    )

    st.markdown("---")

    st.subheader("How It Works")
    st.write(
        """
    1. **Enter** your basic idea
    2. **Customize** with AI suggestions
    3. **Generate** your unique image
    """
    )

    st.markdown("---")

# ________________________

# Visual demo section
st.subheader("✨ See the Difference")

col1, col2, col3 = st.columns([1, 0.3, 1])

with col1:
    st.markdown("### Before")
    st.markdown("**Simple prompt:**")
    st.code("dog in a field", language=None)
    st.image(
        "assets/before_image.png", caption="Generic result", use_container_width=True
    )

with col2:
    st.markdown(
        "<div style='text-align: center; font-size: 3rem; margin-top: 100px;'>→</div>",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown("### After")
    st.markdown("**Enhanced with our tool:**")
    with st.expander("View detailed prompt", expanded=False):
        st.json(
            {
                "subject": "Golden retriever running joyfully",
                "setting": "Sunlit meadow with wildflowers",
                "style": "Photorealistic, high detail, natural colors",
                "lighting": "Golden hour warm glow",
                "details": "Butterflies, distant mountains, soft grass",
            }
        )
    st.image(
        "assets/after_image.png",
        caption="Professional result",
        use_container_width=True,
    )


st.markdown("---")
st.markdown(
    "<h1 style='text-align: center;'>Create Your Image</h1>", unsafe_allow_html=True
)


# ________________________


placeholder_examples = [
    "golden retriever playing in snow",
    "photographer capturing sunset over mountains",
    "woman walking through cyberpunk city street",
    "barista working in cozy coffee shop interior",
    "astronaut riding a horse on alien planet",
    "deer standing in magical forest with glowing mushrooms",
    "couple driving vintage car on desert highway",
    "monk meditating in zen garden with koi pond",
    "pilot navigating steampunk airship through clouds",
    "child watching cat reading a book",
]

if "placeholder_text" not in st.session_state:
    st.session_state.placeholder_text = random.choice(placeholder_examples)

# Step 1: User input
prompt = st.text_input(
    "Enter your image idea:", placeholder=st.session_state.placeholder_text
)

if st.button("Analyze Prompt"):
    if prompt:
        with st.spinner("Analyzing your prompt..."):
            suggestions = analyze_prompt(prompt)

            if suggestions:
                st.success("✅ Analysis complete!")

                # Store suggestions in session state
                st.session_state.suggestions = suggestions
                st.session_state.user_prompt = prompt
                st.session_state.final_prompt = None
            else:
                st.error("Failed to analyze prompt. Please try again.")
    else:
        st.warning("Please enter a prompt first!")

# Step 2: Display suggestions with custom option
if "suggestions" in st.session_state:
    st.divider()
    st.subheader("Choose options for your image:")

    suggestions = st.session_state.suggestions
    selections = {}

    categories = list(suggestions.keys())

    # Display each category
    for idx, category in enumerate(categories):
        options = suggestions[category]

        # Add scroll anchor
        st.markdown(f'<div id="category-{category}"></div>', unsafe_allow_html=True)

        st.write(f"**{category.title()}:**")

        options_with_custom = options + ["✏️ Write your own"]

        current_selection = st.session_state.get(f"selection_{category}", None)

        if current_selection and current_selection in options_with_custom:
            default_index = options_with_custom.index(current_selection)
        else:
            default_index = None

        selected = st.radio(
            f"Select {category}:",
            options_with_custom,
            key=f"radio_{category}",
            label_visibility="collapsed",
            index=default_index,
        )

        # Add to selections dict regardless
        if selected == "✏️ Write your own":
            custom_value = st.text_input(
                f"Enter custom {category}:",
                key=f"custom_{category}",
                placeholder=f"Type your custom {category} here...",
            )
            # Only add if custom value is filled
            if custom_value:
                selections[category] = custom_value
            else:
                selections[category] = selected
        else:
            selections[category] = selected

        # Store the selection and trigger scroll to next category
        if selected and selected != st.session_state.get(f"selection_{category}"):
            st.session_state[f"selection_{category}"] = selected

            # Scroll to next category if there is one
            if idx < len(categories) - 1:
                next_category = categories[idx + 1]
                st.components.v1.html(
                    f"""
                    <script>
                        setTimeout(function() {{
                            const element = window.parent.document.getElementById('category-{next_category}');
                            if (element) {{
                                element.scrollIntoView({{
                                    behavior: 'smooth',
                                    block: 'center'
                                }});
                            }}
                        }}, 100);
                    </script>
                """,
                    height=0,
                )

    # Step 3: Build final prompt button
    st.divider()
    if st.button("Build Final Prompt"):
        # Check if all categories have actual selections
        categories = list(suggestions.keys())
        missing_selections = [
            cat for cat in categories if not st.session_state.get(f"selection_{cat}")
        ]

        # Check if any custom fields are empty
        has_empty_custom = any(v == "✏️ Write your own" for v in selections.values())

        if missing_selections:
            st.warning(
                f"Please select an option for: {', '.join([cat.title() for cat in missing_selections])}"
            )
        elif has_empty_custom:
            st.warning("Please fill in all custom fields or select a different option.")
        else:
            st.session_state.final_prompt = selections
            st.success("✅ Prompt built!")

# Step 4: Display final prompt JSON and generate image
if "final_prompt" in st.session_state and st.session_state.final_prompt:
    st.divider()
    st.subheader("Your Final Prompt:")
    st.json(st.session_state.final_prompt)

    if st.button("Generate Image"):
        with st.spinner("Generating your image... This may take 10-30 seconds."):
            image_bytes, gen_time = generate_image(st.session_state.final_prompt)

            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))

                st.success(f"✅ Image generated in {gen_time:.2f} seconds!")
                st.image(
                    image, caption="Your Generated Image", use_container_width=True
                )

                # Download button
                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png",
                )
            else:
                st.error("Failed to generate image. Please try again.")
