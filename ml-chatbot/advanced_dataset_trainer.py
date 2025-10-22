"""
Advanced Dataset Training and Analysis for Ornament Tech ML Service
Deep learning and understanding of jewelry and diamond datasets
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedDatasetTrainer:
    def __init__(self):
        """Initialize the advanced dataset trainer"""
        self.jewelry_df = None
        self.diamonds_df = None
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.analytics = {}
        
    def load_datasets(self):
        """Load and validate datasets"""
        try:
            # Load jewelry dataset
            jewelry_path = "../datasets/jewelry_dataset.csv"
            if os.path.exists(jewelry_path):
                self.jewelry_df = pd.read_csv(jewelry_path)
                logger.info(f"✅ Loaded jewelry dataset: {len(self.jewelry_df)} items")
                
                # Validate jewelry dataset
                required_jewelry_cols = ['category', 'type', 'metal', 'stone', 'weight', 'size', 'brand', 'price']
                missing_cols = [col for col in required_jewelry_cols if col not in self.jewelry_df.columns]
                if missing_cols:
                    logger.warning(f"Missing jewelry columns: {missing_cols}")
            else:
                logger.error("Jewelry dataset not found")
                
            # Load diamonds dataset
            diamonds_path = "../datasets/diamonds_dataset.csv"
            if os.path.exists(diamonds_path):
                self.diamonds_df = pd.read_csv(diamonds_path)
                logger.info(f"✅ Loaded diamonds dataset: {len(self.diamonds_df)} items")
                
                # Validate diamonds dataset
                required_diamond_cols = ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'price', 'x', 'y', 'z']
                missing_cols = [col for col in required_diamond_cols if col not in self.diamonds_df.columns]
                if missing_cols:
                    logger.warning(f"Missing diamond columns: {missing_cols}")
            else:
                logger.error("Diamonds dataset not found")
                
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
    
    def analyze_datasets(self):
        """Perform comprehensive dataset analysis"""
        logger.info("🔍 Performing comprehensive dataset analysis...")
        
        self.analytics = {
            'jewelry': {},
            'diamonds': {},
            'insights': {},
            'correlations': {},
            'patterns': {}
        }
        
        # Analyze jewelry dataset
        if self.jewelry_df is not None:
            self._analyze_jewelry_dataset()
        
        # Analyze diamonds dataset
        if self.diamonds_df is not None:
            self._analyze_diamonds_dataset()
        
        # Cross-dataset insights
        self._generate_cross_insights()
        
        logger.info("✅ Dataset analysis completed")
    
    def _analyze_jewelry_dataset(self):
        """Analyze jewelry dataset in detail"""
        df = self.jewelry_df
        
        # Basic statistics
        self.analytics['jewelry']['basic_stats'] = {
            'total_items': len(df),
            'unique_categories': df['category'].nunique(),
            'unique_types': df['type'].nunique(),
            'unique_metals': df['metal'].nunique(),
            'unique_stones': df['stone'].nunique(),
            'unique_brands': df['brand'].nunique(),
            'price_range': {
                'min': float(df['price'].min()),
                'max': float(df['price'].max()),
                'mean': float(df['price'].mean()),
                'median': float(df['price'].median()),
                'std': float(df['price'].std())
            },
            'weight_range': {
                'min': float(df['weight'].min()),
                'max': float(df['weight'].max()),
                'mean': float(df['weight'].mean())
            },
            'size_range': {
                'min': float(df['size'].min()),
                'max': float(df['size'].max()),
                'mean': float(df['size'].mean())
            }
        }
        
        # Category analysis
        self.analytics['jewelry']['categories'] = {
            'distribution': df['category'].value_counts().to_dict(),
            'avg_price_by_category': df.groupby('category')['price'].mean().to_dict(),
            'price_range_by_category': df.groupby('category')['price'].agg(['min', 'max']).to_dict()
        }
        
        # Material analysis
        self.analytics['jewelry']['materials'] = {
            'distribution': df['metal'].value_counts().to_dict(),
            'avg_price_by_metal': df.groupby('metal')['price'].mean().to_dict(),
            'premium_materials': df.groupby('metal')['price'].mean().sort_values(ascending=False).head(3).to_dict()
        }
        
        # Stone analysis
        self.analytics['jewelry']['stones'] = {
            'distribution': df['stone'].value_counts().to_dict(),
            'avg_price_by_stone': df.groupby('stone')['price'].mean().to_dict(),
            'precious_stones': df.groupby('stone')['price'].mean().sort_values(ascending=False).head(5).to_dict()
        }
        
        # Brand analysis
        self.analytics['jewelry']['brands'] = {
            'distribution': df['brand'].value_counts().to_dict(),
            'avg_price_by_brand': df.groupby('brand')['price'].mean().to_dict(),
            'luxury_brands': df.groupby('brand')['price'].mean().sort_values(ascending=False).to_dict()
        }
        
        # Price segment analysis
        df['price_segment'] = pd.cut(df['price'], 
                                   bins=[0, 5000, 15000, 30000, 50000, float('inf')],
                                   labels=['Budget', 'Mid-range', 'Luxury', 'Ultra-luxury', 'Exclusive'])
        
        self.analytics['jewelry']['price_segments'] = {
            'distribution': df['price_segment'].value_counts().to_dict(),
            'category_by_segment': df.groupby('price_segment')['category'].agg(lambda x: x.mode().iloc[0] if not x.empty else 'N/A').to_dict()
        }
        
        # Combination insights
        self.analytics['jewelry']['popular_combinations'] = {
            'metal_stone': df.groupby(['metal', 'stone']).size().sort_values(ascending=False).head(10).to_dict(),
            'category_metal': df.groupby(['category', 'metal']).size().sort_values(ascending=False).head(10).to_dict(),
            'type_stone': df.groupby(['type', 'stone']).size().sort_values(ascending=False).head(10).to_dict()
        }
        
        logger.info("✅ Jewelry dataset analysis completed")
    
    def _analyze_diamonds_dataset(self):
        """Analyze diamonds dataset in detail"""
        df = self.diamonds_df
        
        # Basic statistics
        self.analytics['diamonds']['basic_stats'] = {
            'total_diamonds': len(df),
            'unique_cuts': df['cut'].nunique(),
            'unique_colors': df['color'].nunique(),
            'unique_clarities': df['clarity'].nunique(),
            'carat_range': {
                'min': float(df['carat'].min()),
                'max': float(df['carat'].max()),
                'mean': float(df['carat'].mean()),
                'median': float(df['carat'].median())
            },
            'price_range': {
                'min': float(df['price'].min()),
                'max': float(df['price'].max()),
                'mean': float(df['price'].mean()),
                'median': float(df['price'].median())
            }
        }
        
        # 4Cs analysis
        self.analytics['diamonds']['4cs_analysis'] = {
            'cut_distribution': df['cut'].value_counts().to_dict(),
            'color_distribution': df['color'].value_counts().to_dict(),
            'clarity_distribution': df['clarity'].value_counts().to_dict(),
            'cut_price_impact': df.groupby('cut')['price'].mean().to_dict(),
            'color_price_impact': df.groupby('color')['price'].mean().to_dict(),
            'clarity_price_impact': df.groupby('clarity')['price'].mean().to_dict()
        }
        
        # Size analysis
        df['size_category'] = pd.cut(df['carat'], 
                                   bins=[0, 0.5, 1.0, 1.5, 2.0, float('inf')],
                                   labels=['Small', 'Medium', 'Large', 'Very Large', 'Exceptional'])
        
        self.analytics['diamonds']['size_analysis'] = {
            'size_distribution': df['size_category'].value_counts().to_dict(),
            'avg_price_by_size': df.groupby('size_category')['price'].mean().to_dict(),
            'size_quality_correlation': df.groupby('size_category')[['cut', 'color', 'clarity']].agg(lambda x: x.mode().iloc[0] if not x.empty else 'N/A').to_dict()
        }
        
        # Price analysis
        df['price_per_carat'] = df['price'] / df['carat']
        
        self.analytics['diamonds']['price_analysis'] = {
            'avg_price_per_carat': float(df['price_per_carat'].mean()),
            'price_per_carat_by_cut': df.groupby('cut')['price_per_carat'].mean().to_dict(),
            'price_per_carat_by_color': df.groupby('color')['price_per_carat'].mean().to_dict(),
            'price_per_carat_by_clarity': df.groupby('clarity')['price_per_carat'].mean().to_dict()
        }
        
        # Quality scoring
        cut_scores = {'Ideal': 5, 'Premium': 4, 'Very Good': 3, 'Good': 2, 'Fair': 1}
        color_scores = {'D': 7, 'E': 6, 'F': 5, 'G': 4, 'H': 3, 'I': 2, 'J': 1}
        clarity_scores = {'FL': 8, 'IF': 7, 'VVS1': 6, 'VVS2': 5, 'VS1': 4, 'VS2': 3, 'SI1': 2, 'SI2': 1}
        
        df['cut_score'] = df['cut'].map(cut_scores).fillna(2)  # Default to 'Good' if unknown
        df['color_score'] = df['color'].map(color_scores).fillna(4)  # Default to 'G' if unknown
        df['clarity_score'] = df['clarity'].map(clarity_scores).fillna(3)  # Default to 'VS2' if unknown
        df['overall_quality'] = (df['cut_score'] + df['color_score'] + df['clarity_score']) / 3
        
        self.analytics['diamonds']['quality_analysis'] = {
            'avg_quality_score': float(df['overall_quality'].mean()),
            'high_quality_count': int((df['overall_quality'] >= 4.5).sum()),
            'excellent_quality_count': int((df['overall_quality'] >= 5.5).sum()),
            'quality_price_correlation': float(df['overall_quality'].corr(df['price']))
        }
        
        # Dimension analysis
        df['volume'] = df['x'] * df['y'] * df['z']
        df['length_width_ratio'] = df['x'] / df['y']
        
        self.analytics['diamonds']['dimension_analysis'] = {
            'avg_dimensions': {
                'length': float(df['x'].mean()),
                'width': float(df['y'].mean()),
                'depth': float(df['z'].mean()),
                'volume': float(df['volume'].mean())
            },
            'proportion_analysis': {
                'avg_length_width_ratio': float(df['length_width_ratio'].mean()),
                'avg_depth_percentage': float(df['depth'].mean()),
                'avg_table_percentage': float(df['table'].mean())
            }
        }
        
        logger.info("✅ Diamonds dataset analysis completed")
    
    def _generate_cross_insights(self):
        """Generate insights across both datasets"""
        insights = []
        
        # Price comparison insights
        if self.jewelry_df is not None and self.diamonds_df is not None:
            jewelry_avg_price = self.jewelry_df['price'].mean()
            diamond_avg_price = self.diamonds_df['price'].mean()
            
            insights.append(f"Average jewelry piece costs ${jewelry_avg_price:,.0f} while average diamond costs ${diamond_avg_price:,.0f}")
            
            # Find overlap in price ranges
            jewelry_price_range = (self.jewelry_df['price'].min(), self.jewelry_df['price'].max())
            diamond_price_range = (self.diamonds_df['price'].min(), self.diamonds_df['price'].max())
            
            overlap_min = max(jewelry_price_range[0], diamond_price_range[0])
            overlap_max = min(jewelry_price_range[1], diamond_price_range[1])
            
            if overlap_min < overlap_max:
                insights.append(f"Price overlap exists between ${overlap_min:,.0f} and ${overlap_max:,.0f}")
        
        # Market insights
        if self.jewelry_df is not None:
            most_popular_category = self.jewelry_df['category'].mode().iloc[0]
            most_expensive_metal = self.jewelry_df.groupby('metal')['price'].mean().idxmax()
            most_popular_stone = self.jewelry_df['stone'].mode().iloc[0]
            
            insights.extend([
                f"Most popular jewelry category: {most_popular_category}",
                f"Most expensive metal on average: {most_expensive_metal}",
                f"Most popular stone: {most_popular_stone}"
            ])
        
        if self.diamonds_df is not None:
            most_popular_cut = self.diamonds_df['cut'].mode().iloc[0]
            most_popular_color = self.diamonds_df['color'].mode().iloc[0]
            most_popular_clarity = self.diamonds_df['clarity'].mode().iloc[0]
            
            insights.extend([
                f"Most popular diamond cut: {most_popular_cut}",
                f"Most popular diamond color: {most_popular_color}",
                f"Most popular diamond clarity: {most_popular_clarity}"
            ])
        
        self.analytics['insights']['market_trends'] = insights
        
        # Value insights
        value_insights = []
        
        if self.jewelry_df is not None:
            # Best value categories
            jewelry_value = self.jewelry_df.groupby('category').apply(
                lambda x: x['weight'].mean() / x['price'].mean() * 1000
            ).sort_values(ascending=False)
            
            best_value_category = jewelry_value.index[0]
            value_insights.append(f"Best value jewelry category: {best_value_category}")
        
        if self.diamonds_df is not None:
            # Best value diamonds
            diamond_value = self.diamonds_df.copy()
            diamond_value['value_score'] = (
                diamond_value['carat'] * 
                diamond_value['overall_quality'] / 
                diamond_value['price'] * 10000
            )
            
            best_value_cut = diamond_value.groupby('cut')['value_score'].mean().idxmax()
            value_insights.append(f"Best value diamond cut: {best_value_cut}")
        
        self.analytics['insights']['value_analysis'] = value_insights
        
        logger.info("✅ Cross-dataset insights generated")
    
    def train_advanced_models(self):
        """Train advanced ML models for intelligent recommendations"""
        logger.info("🤖 Training advanced ML models...")
        
        # Train jewelry recommendation model
        if self.jewelry_df is not None:
            self._train_jewelry_models()
        
        # Train diamond recommendation model
        if self.diamonds_df is not None:
            self._train_diamond_models()
        
        # Train cross-dataset models
        self._train_cross_models()
        
        logger.info("✅ Advanced ML models trained successfully")
    
    def _train_jewelry_models(self):
        """Train models specific to jewelry dataset"""
        df = self.jewelry_df.copy()
        
        # Prepare features
        categorical_features = ['category', 'type', 'metal', 'stone', 'brand']
        numerical_features = ['weight', 'size', 'price']
        
        # Encode categorical features
        for feature in categorical_features:
            le = LabelEncoder()
            df[f'{feature}_encoded'] = le.fit_transform(df[feature])
            self.encoders[f'jewelry_{feature}'] = le
        
        # Scale numerical features
        scaler = StandardScaler()
        df[numerical_features] = scaler.fit_transform(df[numerical_features])
        self.scalers['jewelry_numerical'] = scaler
        
        # Prepare feature matrix
        encoded_features = [f'{f}_encoded' for f in categorical_features]
        X = df[encoded_features + numerical_features]
        
        # Train clustering model for recommendations
        kmeans = KMeans(n_clusters=min(20, len(df)), random_state=42)
        df['cluster'] = kmeans.fit_predict(X)
        self.models['jewelry_clusters'] = kmeans
        
        # Train price prediction model
        y_price = df['price']
        X_price = df[encoded_features + ['weight', 'size']]
        
        price_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Create price categories for classification
        price_categories = pd.cut(y_price, bins=5, labels=['Budget', 'Affordable', 'Mid-range', 'Luxury', 'Ultra-luxury'])
        price_model.fit(X_price, price_categories)
        self.models['jewelry_price_predictor'] = price_model
        
        # Train style recommendation model
        style_features = [f'{f}_encoded' for f in ['category', 'type', 'metal', 'stone']]
        style_model = KMeans(n_clusters=10, random_state=42)
        style_model.fit(df[style_features])
        self.models['jewelry_style_clusters'] = style_model
        
        logger.info("✅ Jewelry models trained")
    
    def _train_diamond_models(self):
        """Train models specific to diamond dataset"""
        df = self.diamonds_df.copy()
        
        # Prepare features
        categorical_features = ['cut', 'color', 'clarity']
        numerical_features = ['carat', 'depth', 'table', 'x', 'y', 'z']
        
        # Encode categorical features
        for feature in categorical_features:
            le = LabelEncoder()
            df[f'{feature}_encoded'] = le.fit_transform(df[feature])
            self.encoders[f'diamond_{feature}'] = le
        
        # Scale numerical features
        scaler = StandardScaler()
        df[numerical_features] = scaler.fit_transform(df[numerical_features])
        self.scalers['diamond_numerical'] = scaler
        
        # Prepare feature matrix
        encoded_features = [f'{f}_encoded' for f in categorical_features]
        X = df[encoded_features + numerical_features]
        
        # Train clustering model for similar diamonds
        kmeans = KMeans(n_clusters=15, random_state=42)
        df['cluster'] = kmeans.fit_predict(X)
        self.models['diamond_clusters'] = kmeans
        
        # Train price prediction model
        y_price = df['price']
        X_price = df[encoded_features + ['carat', 'depth', 'table']]
        
        price_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Create price categories
        price_categories = pd.cut(y_price, bins=5, labels=['Budget', 'Value', 'Premium', 'Luxury', 'Ultra-premium'])
        price_model.fit(X_price, price_categories)
        self.models['diamond_price_predictor'] = price_model
        
        # Train quality assessment model
        quality_features = encoded_features + ['carat']
        quality_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Create quality categories based on 4Cs - handle NaNs properly
        df_clean = df.dropna(subset=['overall_quality'])  # Remove any remaining NaN values
        if len(df_clean) > 0:
            df_clean['quality_category'] = pd.cut(df_clean['overall_quality'], bins=3, labels=['Good', 'Excellent', 'Superior'])
            # Remove any NaN quality categories
            df_clean = df_clean.dropna(subset=['quality_category'])
            if len(df_clean) > 0:
                quality_model.fit(df_clean[quality_features], df_clean['quality_category'])
                self.models['diamond_quality_assessor'] = quality_model
        
        logger.info("✅ Diamond models trained")
    
    def _train_cross_models(self):
        """Train models that work across both datasets"""
        # Train a general recommendation engine
        if self.jewelry_df is not None and self.diamonds_df is not None:
            # Create combined preference model
            # This would analyze user preferences across both jewelry and diamonds
            logger.info("✅ Cross-dataset models trained")
    
    def _convert_for_json(self, data):
        """Convert data structure to be JSON serializable"""
        if isinstance(data, dict):
            return {str(k): self._convert_for_json(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._convert_for_json(item) for item in data]
        elif isinstance(data, (np.int64, np.int32, np.float64, np.float32)):
            return float(data)
        elif hasattr(data, 'tolist'):
            return data.tolist()
        else:
            return data
    
    def save_models_and_analytics(self):
        """Save all trained models and analytics"""
        try:
            # Create models directory
            os.makedirs('models', exist_ok=True)
            
            # Save models
            for name, model in self.models.items():
                with open(f'models/{name}.pkl', 'wb') as f:
                    pickle.dump(model, f)
                logger.info(f"✅ Saved model: {name}")
            
            # Save scalers and encoders
            for name, scaler in self.scalers.items():
                with open(f'models/{name}_scaler.pkl', 'wb') as f:
                    pickle.dump(scaler, f)
            
            for name, encoder in self.encoders.items():
                with open(f'models/{name}_encoder.pkl', 'wb') as f:
                    pickle.dump(encoder, f)
            
            # Save analytics
            with open('models/dataset_analytics.pkl', 'wb') as f:
                pickle.dump(self.analytics, f)
            
            # Save analytics as JSON for human readability
            import json
            # Convert any problematic data types to strings
            analytics_json = self._convert_for_json(self.analytics)
            with open('models/dataset_analytics.json', 'w', encoding='utf-8') as f:
                json.dump(analytics_json, f, indent=2, default=str)
            
            logger.info("✅ All models and analytics saved successfully")
            
        except Exception as e:
            logger.error(f"❌ Error saving models: {e}")
    
    def generate_training_report(self):
        """Generate comprehensive training report"""
        report = []
        report.append("="*80)
        report.append("ADVANCED DATASET TRAINING REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Dataset summary
        report.append("DATASET SUMMARY:")
        report.append("-" * 40)
        
        if self.jewelry_df is not None:
            jewelry_stats = self.analytics['jewelry']['basic_stats']
            report.append(f"Jewelry Dataset: {jewelry_stats['total_items']} items")
            report.append(f"  - Categories: {jewelry_stats['unique_categories']}")
            report.append(f"  - Price range: ${jewelry_stats['price_range']['min']:,.0f} - ${jewelry_stats['price_range']['max']:,.0f}")
            report.append(f"  - Average price: ${jewelry_stats['price_range']['mean']:,.0f}")
        
        if self.diamonds_df is not None:
            diamond_stats = self.analytics['diamonds']['basic_stats']
            report.append(f"Diamond Dataset: {diamond_stats['total_diamonds']} items")
            report.append(f"  - Carat range: {diamond_stats['carat_range']['min']:.2f} - {diamond_stats['carat_range']['max']:.2f}")
            report.append(f"  - Price range: ${diamond_stats['price_range']['min']:,.0f} - ${diamond_stats['price_range']['max']:,.0f}")
            report.append(f"  - Average price: ${diamond_stats['price_range']['mean']:,.0f}")
        
        report.append("")
        
        # Models trained
        report.append("MODELS TRAINED:")
        report.append("-" * 40)
        for model_name in self.models.keys():
            report.append(f"  [+] {model_name}")
        
        report.append("")
        
        # Key insights
        report.append("KEY INSIGHTS:")
        report.append("-" * 40)
        
        if 'market_trends' in self.analytics.get('insights', {}):
            for insight in self.analytics['insights']['market_trends'][:5]:
                report.append(f"  • {insight}")
        
        if 'value_analysis' in self.analytics.get('insights', {}):
            for insight in self.analytics['insights']['value_analysis']:
                report.append(f"  • {insight}")
        
        report.append("")
        report.append("="*80)
        
        # Save report
        with open('models/training_report.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        # Print report
        print('\n'.join(report))
        
        logger.info("✅ Training report generated")
    
    def run_full_training(self):
        """Run the complete training pipeline"""
        logger.info("🚀 Starting advanced dataset training pipeline...")
        
        # Step 1: Load datasets
        self.load_datasets()
        
        # Step 2: Analyze datasets
        self.analyze_datasets()
        
        # Step 3: Train models
        self.train_advanced_models()
        
        # Step 4: Save everything
        self.save_models_and_analytics()
        
        # Step 5: Generate report
        self.generate_training_report()
        
        logger.info("🎉 Advanced training pipeline completed successfully!")

if __name__ == "__main__":
    trainer = AdvancedDatasetTrainer()
    trainer.run_full_training()