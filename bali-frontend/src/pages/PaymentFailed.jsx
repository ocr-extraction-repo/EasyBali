import { useCallback, useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

const PaymentFailed = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const orderNumber = searchParams.get("order");
  const supportNumber = String(import.meta.env.VITE_SUPPORT_WHATSAPP_NUMBER || "").replace(/\D/g, "");
  const supportHref = supportNumber ? `https://wa.me/${supportNumber}` : null;

  const [loading, setLoading] = useState(false);
  const [recoveryOptions, setRecoveryOptions] = useState(null);
  const [error, setError] = useState(null);

  const fetchRecoveryOptions = useCallback(async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/payment/recovery-options/${orderNumber}`);
      setRecoveryOptions(response.data.options);
    } catch {
      setError("Unable to fetch payment details. Please contact support.");
    }
  }, [orderNumber]);

  useEffect(() => {
    if (orderNumber) {
      fetchRecoveryOptions();
    }
  }, [orderNumber, fetchRecoveryOptions]);

  const handleRegenerateLink = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/payment/regenerate/${orderNumber}`);
      if (response.data.success) {
        window.location.href = response.data.payment_url;
      } else {
        setError(response.data.error || "Failed to regenerate payment link");
      }
    } catch {
      setError("Error regenerating payment link. Please try again or contact support.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center">
            <svg className="w-12 h-12 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 text-center mb-4">
          Payment {recoveryOptions?.current_status === "expired" ? "Expired" : "Failed"}
        </h1>

        {orderNumber && (
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <p className="text-sm text-gray-600 mb-1">Order Number</p>
            <p className="font-mono font-bold text-gray-900">{orderNumber}</p>
          </div>
        )}

        {recoveryOptions?.failure_reason && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-yellow-800">
              <strong>Reason:</strong> {recoveryOptions.failure_reason}
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        )}

        {recoveryOptions && (
          <div className="space-y-4">
            {recoveryOptions.can_regenerate && (
              <>
                <p className="text-gray-600 text-center mb-4">
                  {recoveryOptions.current_status === "expired"
                    ? "Your payment link has expired. Generate a new link to complete your booking."
                    : "Your payment failed. Generate a fresh link to complete your booking."}
                </p>

                <button
                  onClick={handleRegenerateLink}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Generating..." : "Generate New Payment Link"}
                </button>
              </>
            )}

            {!recoveryOptions.can_regenerate && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                <p className="text-sm text-blue-800">
                  Current status: <strong>{recoveryOptions.current_status}</strong>
                </p>
                {recoveryOptions.payment_url && (
                  <a
                    href={recoveryOptions.payment_url}
                    className="text-blue-600 underline text-sm mt-2 block"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View existing payment link
                  </a>
                )}
              </div>
            )}

            <button
              onClick={() => navigate("/")}
              className="w-full bg-white border-2 border-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-lg hover:bg-gray-50 transition-all duration-200"
            >
              Return to Home
            </button>

            <div className="text-center pt-4 border-t border-gray-200">
              <p className="text-sm text-gray-600 mb-2">Need help?</p>
              {supportHref ? (
                <a
                  href={supportHref}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-green-600 font-semibold hover:text-green-700"
                >
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                  </svg>
                  Contact Support
                </a>
              ) : (
                <p className="text-xs text-gray-500">Support contact is not configured.</p>
              )}
            </div>
          </div>
        )}

        {!recoveryOptions && !error && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
            <p className="text-gray-600 mt-4">Loading payment details...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentFailed;
