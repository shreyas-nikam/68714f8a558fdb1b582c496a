
import streamlit as st
from application_pages.analyze_data import calculate_control_quality_score, suggest_substantiation_method

def run_evaluate_control():
    st.header("Evaluate Control")
    
    # Add comprehensive introduction
    st.markdown("""
    **Welcome to the Control Evaluation Tool!** This interactive assessment helps you analyze individual controls 
    by defining their key attributes and calculating both a **Control Quality Score** and a recommended 
    **Control Substantiation Method** for audit testing.
    
    Use this tool to:
    - **Assess control strength** through systematic scoring
    - **Determine appropriate testing methods** based on risk and characteristics  
    - **Benchmark controls** against industry best practices
    - **Identify improvement opportunities** for control design and implementation
    """)
    
    # Add expandable methodology section
    with st.expander("**Methodology & Scoring Guide**", expanded=False):
        st.markdown("""
        ### Control Quality Score Calculation
        
        The Control Quality Score is calculated using a weighted scoring system:
        
        | **Attribute** | **Score Range** | **Details** |
        |---------------|-----------------|-------------|
        | **Control Type** | +2 to +5 | Preventative (+5), Detective (+2) |
        | **Key Classification** | +1 to +3 | Key (+3), Non-Key (+1) |
        | **Automation Level** | +1 to +2 | Automated (+2), Manual (+1) |
        | **Implementation Quality** | +0 to +4 | Rating 1-5 (adds 0-4 points) |
        
        **Total Score Range: 4-14 points**
        - 🟢 **12-14**: Excellent (Strong, well-designed controls)
        - 🟡 **8-11**: Good (Solid controls with minor improvements needed)
        - 🟠 **6-7**: Fair (Moderate effectiveness, improvement recommended)
        - 🔴 **4-5**: Poor (Significant weaknesses, immediate attention required)
        
        ### Substantiation Method Selection
        
        Testing methods are recommended based on control characteristics and risk level:
        
        - **Re-performance**: Execute the control procedure independently
        - **Examination**: Review evidence and documentation
        - **Inquiry**: Interview control performers and review process
        - **Combination**: Multiple methods for complex or high-risk controls
        """)
    
    st.divider()
    
    # Enhanced control input section with detailed explanations
    st.subheader("Control Attributes")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### **Control Characteristics**")
        
        control_types = ["Preventative", "Detective"]
        control_type = st.selectbox(
            "**Control Type**", 
            options=control_types, 
            help="Defines the control's primary function in risk management."
        )
        
        # Add detailed explanation based on selection
        if control_type == "Preventative":
            st.info("**Preventative Control**: Designed to prevent errors or irregularities before they occur. Examples: authorization requirements, segregation of duties, system access controls.")
        else:
            st.info("**Detective Control**: Identifies issues after they have occurred. Examples: reconciliations, variance analysis, monitoring reports.")
        
        key_nonkey_options = ["Key", "Non-Key"]
        key_nonkey = st.selectbox(
            "**Key/Non-Key Classification**", 
            options=key_nonkey_options, 
            help="Determines the control's criticality in your risk management framework."
        )
        
        if key_nonkey == "Key":
            st.warning("**Key Control**: Critical for preventing or detecting material misstatements. Requires rigorous testing and cannot be bypassed without alternative compensating controls.")
        else:
            st.info("**Non-Key Control**: Provides additional assurance but failure alone would not result in material risk. Often works in combination with other controls.")
    
    with col2:
        st.markdown("#### **Implementation Details**")
        
        manual_automated_options = ["Manual", "Automated"]
        manual_automated = st.selectbox(
            "**Execution Method**", 
            options=manual_automated_options, 
            help="How the control is performed - manually by people or automatically by systems."
        )
        
        if manual_automated == "Automated":
            st.success("**Automated Control**: Executed by systems with minimal human intervention. Generally more reliable and consistent, but requires strong IT controls.")
        else:
            st.warning("**Manual Control**: Performed by people. Offers flexibility but subject to human error. Requires proper training and supervision.")
        
        risk_level_options = ["High", "Medium", "Low"]
        risk_level = st.selectbox(
            "**Associated Risk Level**", 
            options=risk_level_options, 
            help="The inherent risk level that this control is designed to mitigate."
        )
        
        risk_descriptions = {
            "High": "High impact potential requiring intensive monitoring and testing",
            "Medium": "Moderate impact requiring regular monitoring", 
            "Low": "Lower impact allowing for lighter testing procedures"
        }
        st.info(f"**{risk_level} Risk**: {risk_descriptions[risk_level]}")
    
    st.divider()
    
    # Implementation Quality Rating with enhanced explanation
    st.subheader("Implementation Quality Assessment")
    st.markdown("""
    Rate the observed quality of how this control is currently implemented and executed:
    """)
    
    implementation_quality_rating = st.slider(
        "**Implementation Quality Rating**", 
        min_value=1, 
        max_value=5, 
        step=1, 
        help="Assess the current effectiveness of control execution (1 = Poor, 5 = Excellent)"
    )
    
    # Quality rating explanations
    quality_descriptions = {
        1: "**Poor (1)**: Significant deficiencies, control frequently fails or is bypassed",
        2: "**Below Average (2)**: Notable weaknesses, inconsistent execution",
        3: "**Average (3)**: Generally effective with some minor issues",
        4: "**Good (4)**: Well-executed with minimal deficiencies", 
        5: "**Excellent (5)**: Exemplary implementation, no identified weaknesses"
    }
    
    st.info(quality_descriptions[implementation_quality_rating])
    
    st.divider()
    
    # Enhanced calculation section
    if st.button("**Calculate Score & Substantiation Method**", type="primary"):
        try:
            control_quality_score = calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating)
            substantiation_method = suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level)
            
            st.divider()
            st.subheader("**Evaluation Results**")
            
            # Display results in enhanced format
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### **Control Quality Score**")
                
                # Color-code the score based on ranges
                if control_quality_score >= 12:
                    st.success(f"**Score: {control_quality_score}/14** 🌟")
                    st.success("**Rating: Excellent** - Strong, well-designed control")
                elif control_quality_score >= 8:
                    st.info(f"**Score: {control_quality_score}/14** ✅")
                    st.info("**Rating: Good** - Solid control with minor improvements needed")
                elif control_quality_score >= 6:
                    st.warning(f"**Score: {control_quality_score}/14** ⚠️")
                    st.warning("**Rating: Fair** - Moderate effectiveness, improvement recommended")
                else:
                    st.error(f"**Score: {control_quality_score}/14** ❌")
                    st.error("**Rating: Poor** - Significant weaknesses, immediate attention required")
                
                # Score breakdown
                with st.expander("**Score Breakdown**"):
                    control_points = 5 if control_type == "Preventative" else 2
                    key_points = 3 if key_nonkey == "Key" else 1
                    auto_points = 2 if manual_automated == "Automated" else 1
                    impl_points = implementation_quality_rating - 1
                    
                    st.write(f"• **Control Type ({control_type}):** +{control_points} points")
                    st.write(f"• **Classification ({key_nonkey}):** +{key_points} points")
                    st.write(f"• **Execution ({manual_automated}):** +{auto_points} points")
                    st.write(f"• **Implementation Quality:** +{impl_points} points")
                    st.write(f"**Total Score:** {control_quality_score} points")
            
            with col2:
                st.markdown("#### **Recommended Testing Method**")

                # Enhanced substantiation method display
                method_icons = {
                    "Re-performance": "🔄",
                    "Examination": "📋", 
                    "Inquiry": "❓",
                    "Re-performance / Examination": "🔍"
                }
                
                icon = method_icons.get(substantiation_method, "🧪")
                st.info(f"**{icon} {substantiation_method}**")
                
                # Detailed method explanations
                method_explanations = {
                    "Re-performance": {
                        "description": "Execute the control procedure independently to verify it operates as designed.",
                        "when": "High-risk controls, key manual processes, complex calculations",
                        "effort": "High",
                        "reliability": "Highest"
                    },
                    "Examination": {
                        "description": "Review and analyze evidence, documentation, and supporting materials.",
                        "when": "Automated controls, documented processes, system-generated reports", 
                        "effort": "Medium",
                        "reliability": "Good"
                    },
                    "Inquiry": {
                        "description": "Interview control performers and review process documentation.",
                        "when": "Low-risk controls, well-established processes, preliminary assessment",
                        "effort": "Low", 
                        "reliability": "Moderate"
                    },
                    "Re-performance / Examination": {
                        "description": "Combination approach using multiple testing methods for comprehensive coverage.",
                        "when": "Critical controls with high complexity or risk",
                        "effort": "High",
                        "reliability": "Highest"
                    }
                }
                
                if substantiation_method in method_explanations:
                    details = method_explanations[substantiation_method]
                    st.markdown(f"**Description:** {details['description']}")
                    st.markdown(f"**Best used when:** {details['when']}")
                    st.markdown(f"**Testing effort:** {details['effort']}")
                    st.markdown(f"**Evidence reliability:** {details['reliability']}")
            
            # Additional insights and recommendations
            st.divider()
            st.subheader("**Insights & Recommendations**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### **Control Strengths**")
                strengths = []
                
                if control_type == "Preventative":
                    strengths.append("Proactive risk prevention approach")
                if key_nonkey == "Key":
                    strengths.append("Critical control for risk mitigation")
                if manual_automated == "Automated":
                    strengths.append("Reduced human error through automation")
                if implementation_quality_rating >= 4:
                    strengths.append("High implementation quality")
                if control_quality_score >= 10:
                    strengths.append("Strong overall control design")

                if strengths:
                    for strength in strengths:
                        st.write(strength)
                else:
                    st.write("Consider the improvement opportunities to enhance control effectiveness.")
            
            with col2:
                st.markdown("#### **Improvement Opportunities**")
                improvements = []
                
                if control_type == "Detective":
                    improvements.append("Consider preventative controls to address root causes")
                if key_nonkey == "Non-Key" and risk_level == "High":
                    improvements.append("Evaluate if this should be classified as a Key control")
                if manual_automated == "Manual" and risk_level in ["High", "Medium"]:
                    improvements.append("Explore automation opportunities")
                if implementation_quality_rating <= 2:
                    improvements.append("Address implementation quality issues immediately")
                if control_quality_score < 8:
                    improvements.append("Consider control redesign or enhancement")
                
                if improvements:
                    for improvement in improvements:
                        st.write(improvement)
                else:
                    st.write("Well-designed control with strong implementation!")
            
            # Benchmarking section
            st.divider() 
            st.subheader("**Benchmarking Context**")
            
            benchmark_data = {
                "Industry Average": 8.5,
                "Best Practice": 12.0,
                "Regulatory Minimum": 6.0,
                "Your Control": control_quality_score
            }
            
            st.markdown("**How your control compares:**")
            for label, score in benchmark_data.items():
                if label == "Your Control":
                    if score >= benchmark_data["Best Practice"]:
                        st.success(f"**{label}:** {score} (Exceeds best practice)")
                    elif score >= benchmark_data["Industry Average"]:
                        st.info(f"**{label}:** {score} (Above average)")
                    elif score >= benchmark_data["Regulatory Minimum"]:
                        st.warning(f"**{label}:** {score} (Meets minimum standards)")
                    else:
                        st.error(f"**{label}:** {score} (Below minimum standards)")
                else:
                    st.write(f"**{label}:** {score}")

        except Exception as e:
            st.error(f"**An error occurred during calculation:** {e}")
            st.info("Please check your inputs and try again. If the issue persists, contact support.")
    
    # Add helpful tips section
    st.divider()
    with st.expander("**Tips for Effective Control Evaluation**", expanded=False):
        st.markdown("""
        ### **Best Practices for Control Assessment**
        
        **Before You Start:**
        - Gather complete control documentation
        - Understand the control's business purpose
        - Review any historical testing results
        - Interview control performers when possible

        **During Assessment:**
        - Be objective in your quality rating
        - Consider the control's operating history
        - Evaluate effectiveness, not just design
        - Document your reasoning for ratings

        **After Results:**
        - Validate findings with control owners
        - Plan follow-up actions for improvements
        - Monitor control performance over time
        - Re-evaluate after any changes

        ### **Common Control Enhancement Strategies**

        - **Automation:** Reduce manual effort and human error
        - **Monitoring:** Add detective layers to preventative controls
        - **Training:** Improve manual control execution quality
        - **Documentation:** Strengthen control procedures and guidance
        - **Testing:** Regular validation of control effectiveness
        """)
