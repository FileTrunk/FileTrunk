import { useState } from "react";
import share_icon from "./pictures/share-icon.png";
import api from "../../service/Api";
import { CopyToClipboard } from "react-copy-to-clipboard";

const Share = ({
  object_id,
  link_for_sharing,
  setTime,
  setShareLink,
  setFileIdState,
  onShare,
  onDelete,
  time,
}) => {
  return (
    <div>
      <img
        src={share_icon}
        alt="Share"
        className="icon d-flex align-items-end"
        data-toggle="modal"
        data-target="#shareLinkForm"
        onClick={() => {
          setFileIdState(object_id);
          setShareLink(false);
        }}
      />
      <div
        className="modal fade"
        id="shareLinkForm"
        tabIndex="-1"
        role="dialog"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="exampleModalLongTitle">
                Choose a time when this link will expire
              </h5>
              <button
                type="button"
                className="close"
                data-dismiss="modal"
                aria-label="Close"
              >
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <form>
                <div className="mb-2 w-25 float-start">
                  <select
                    type="input"
                    onChange={(e) => {
                      setTime(e.target.value);
                    }}
                    defaultValue={time}
                  >
                    <option value="1">1 minute</option>
                    <option value="5">5 minute</option>
                    <option value="10">10 minutes</option>
                    <option value="30">30 minutes</option>
                    <option value="60">1 hour</option>
                    <option value="360">6 hours</option>
                  </select>
                </div>
              </form>
              {link_for_sharing && (
                <div>
                  <h6>{link_for_sharing}</h6>
                  <CopyToClipboard text={link_for_sharing}>
                    <button className="btn btn-primary">
                      Copy to clipboard
                    </button>
                  </CopyToClipboard>
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                data-dismiss="modal"
                onClick={() => {
                  setShareLink(false);
                }}
              >
                Close
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  setShareLink(false);
                  onDelete();
                }}
              >
                Disable all links
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  setShareLink(false);
                  onShare();
                }}
              >
                Generate
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Share;
