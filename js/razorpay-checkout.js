'use strict';

(() => {
  const form = document.getElementById('payment-form');
  if (!form) return;

  const button = document.getElementById('pay-button');
  const buttonLabel = document.getElementById('pay-button-label');
  const status = document.getElementById('payment-status');

  function showStatus(message, isError) {
    status.textContent = message;
    status.style.display = 'block';
    status.style.color = isError ? '#b42318' : 'var(--text-dim)';
  }

  function setBusy(busy, label) {
    button.disabled = busy;
    buttonLabel.textContent = label || (busy ? 'Connecting to Razorpay…' : 'Pay ₹1.00 securely');
    button.style.opacity = busy ? '0.7' : '1';
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    if (!window.Razorpay) {
      showStatus('The secure checkout could not load. Refresh this page or contact IYONEX.', true);
      return;
    }

    const payer = {
      name: document.getElementById('payer-name').value.trim(),
      email: document.getElementById('payer-email').value.trim()
    };

    setBusy(true, 'Creating secure order…');
    showStatus('Connecting securely to Razorpay. Do not refresh this page.', false);

    try {
      const orderResponse = await fetch('/api/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payer)
      });
      const order = await orderResponse.json();
      if (!orderResponse.ok) throw new Error(order.error || 'Could not create a payment order.');

      const options = {
        key: order.key_id,
        amount: order.amount,
        currency: order.currency,
        name: 'IYONEX Automation Private Limited',
        description: 'Embedded Systems Internship — one-rupee live gateway test',
        order_id: order.order_id,
        prefill: { name: payer.name, email: payer.email },
        notes: { reference: 'ESI-1M-LIVE-TEST' },
        theme: { color: '#2563eb' },
        handler: async function (response) {
          setBusy(true, 'Verifying payment…');
          showStatus('Payment response received. Verifying it with IYONEX and Razorpay…', false);
          try {
            const verifyResponse = await fetch('/api/verify-payment', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ ...response, order_token: order.order_token })
            });
            const result = await verifyResponse.json();

            if (result.paid === true && result.verified === true) {
              showStatus(
                '₹1 live payment captured and verified. This confirms the Razorpay gateway test only, not internship admission. Payment ID: ' + result.payment_id + '. Please retain this confirmation.',
                false
              );
              form.reset();
            } else if (result.verified === true) {
              showStatus(
                'The payment signature is valid, but the payment is not yet captured by Razorpay. Status: ' +
                (result.payment_status || 'pending') +
                '. Please do not pay again. Contact IYONEX with your payment ID: ' + (response.razorpay_payment_id || 'pending'),
                false
              );
            } else {
              throw new Error(result.error || 'Payment verification failed. Do not retry until IYONEX checks the payment.');
            }
          } catch (error) {
            showStatus(error.message || 'Payment verification could not be completed. Do not pay again; contact IYONEX with your invoice reference.', true);
          } finally {
            setBusy(false);
          }
        },
        modal: {
          ondismiss: function () {
            setBusy(false);
            showStatus('Checkout was closed. No payment confirmation was received. You can try again after checking your Razorpay payment status.', false);
          }
        }
      };

      const checkout = new window.Razorpay(options);
      checkout.on('payment.failed', function (failure) {
        setBusy(false);
        const reason = failure && failure.error && failure.error.description
          ? failure.error.description
          : 'The payment could not be completed.';
        showStatus(reason + ' No successful payment was confirmed. Check your Razorpay payment status before trying again.', true);
      });
      checkout.open();
      setBusy(false, 'Secure checkout opened');
    } catch (error) {
      setBusy(false);
      showStatus(error.message || 'Unable to start checkout. Please try again or contact IYONEX.', true);
    }
  });
})();
