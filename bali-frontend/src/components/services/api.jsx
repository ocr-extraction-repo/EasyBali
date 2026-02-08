const BASE_URL = import.meta.env.VITE_BASE_URL || 'https://easy-bali.onrender.com';

export const getSubMenu = async (mainMenu) => {
  try {
    const response = await fetch(`${BASE_URL}/menu/sub/${encodeURIComponent(mainMenu)}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching submenu:', error);
    throw error;
  }
};


export const getSubCategory = async (category) => {
  try {
    const response = await fetch(`${BASE_URL}/menu/sub-category/${encodeURIComponent(category)}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching subcategory:', error);
    throw error;
  }
};


export const getServiceItems = async (category) => {
  try {
    const response = await fetch(`${BASE_URL}/menu/service-items/${encodeURIComponent(category)}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching subcategory:', error);
    throw error;
  }
};